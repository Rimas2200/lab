import mysql.connector
from mysql.connector import errorcode
from tabulate import tabulate
import uuid
from datetime import datetime, timedelta
import random

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'pawnshop_db',
}

# Подключение
try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Ошибка логина или пароля")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("База данных не существует")
    else:
        print(err)
else:
    print("Подключено к базе данных")


def create_tables():
    TABLES = {}

    # Таблица клиентов
    TABLES['clients'] = """
    CREATE TABLE IF NOT EXISTS clients (
      client_id INT PRIMARY KEY AUTO_INCREMENT,
      surname VARCHAR(50),
      name VARCHAR(50),
      patronymic VARCHAR(50),
      birth_date DATE,
      passport_series VARCHAR(10),
      passport_number VARCHAR(20),
      passport_issued_by VARCHAR(255),
      passport_issue_date DATE,
      residence_address VARCHAR(255),
      registration_address VARCHAR(255),
      phone INT(10),
      email VARCHAR(100),
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB;
    """

    # Типы металлов
    TABLES['metal_types'] = """
    CREATE TABLE IF NOT EXISTS metal_types (
      metal_type_id INT PRIMARY KEY AUTO_INCREMENT,
      type_name VARCHAR(50) NOT NULL UNIQUE
    ) ENGINE=InnoDB;
    """

    # Типы вставок
    TABLES['inlay_types'] = """
    CREATE TABLE IF NOT EXISTS inlay_types (
      inlay_type_id INT PRIMARY KEY AUTO_INCREMENT,
      type_name VARCHAR(50) NOT NULL UNIQUE
    ) ENGINE=InnoDB;
    """

    # Ценности
    TABLES['valuables'] = """
    CREATE TABLE IF NOT EXISTS valuables (
      valuable_id INT PRIMARY KEY AUTO_INCREMENT,
      client_id INT,
      metal_type_id INT,
      inlay_type_id INT,
      weight DECIMAL(10,3),
      purity DECIMAL(5,2),
      description TEXT,
      appraised_value DECIMAL(15,2),
      received_date DATE,
      storage_location VARCHAR(100),
      FOREIGN KEY (client_id) REFERENCES clients (client_id),
      FOREIGN KEY (metal_type_id) REFERENCES metal_types (metal_type_id),
      FOREIGN KEY (inlay_type_id) REFERENCES inlay_types (inlay_type_id)
    ) ENGINE=InnoDB;
    """

    # Ломбарды
    TABLES['pawnshops'] = """
    CREATE TABLE IF NOT EXISTS pawnshops (
      pawnshop_id INT PRIMARY KEY AUTO_INCREMENT,
      name VARCHAR(100),
      address VARCHAR(255),
      phone VARCHAR(20),
      email VARCHAR(100),
      working_hours VARCHAR(50),
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB;
    """

    # Сотрудники
    TABLES['employees'] = """
    CREATE TABLE IF NOT EXISTS employees (
      employee_id INT PRIMARY KEY AUTO_INCREMENT,
      pawnshop_id INT,
      surname VARCHAR(50),
      name VARCHAR(50),
      patronymic VARCHAR(50),
      position VARCHAR(50),
      phone VARCHAR(20),
      email VARCHAR(100),
      hire_date DATE,
      FOREIGN KEY (pawnshop_id) REFERENCES pawnshops (pawnshop_id)
    ) ENGINE=InnoDB;
    """

    # Залоги
    TABLES['pledges'] = """
    CREATE TABLE IF NOT EXISTS pledges (
      pledge_id INT PRIMARY KEY AUTO_INCREMENT,
      valuable_id INT,
      pawnshop_id INT,
      employee_id INT,
      pledge_date DATE,
      end_date DATE,
      loan_amount DECIMAL(15,2),
      interest_rate DECIMAL(5,2),
      status ENUM ('Активный', 'Выкуплен', 'Продан') DEFAULT 'Активный',
      comments TEXT,
      FOREIGN KEY (valuable_id) REFERENCES valuables (valuable_id),
      FOREIGN KEY (pawnshop_id) REFERENCES pawnshops (pawnshop_id),
      FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
    ) ENGINE=InnoDB;
    """

    # Платежи
    TABLES['payments'] = """
    CREATE TABLE IF NOT EXISTS payments (
      payment_id INT PRIMARY KEY AUTO_INCREMENT,
      pledge_id INT,
      employee_id INT,
      payment_date DATE,
      amount DECIMAL(15,2),
      payment_type ENUM ('Частичная выплата', 'Полный выкуп'),
      comments TEXT,
      FOREIGN KEY (pledge_id) REFERENCES pledges (pledge_id),
      FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
    ) ENGINE=InnoDB;
    """

    # Создание таблиц
    for table_name in TABLES:
        table_sql = TABLES[table_name]
        try:
            print(f"Создаётся таблица {table_name}...")
            cursor.execute(table_sql)
        except mysql.connector.Error as err:
            print(f"Ошибка при создании таблицы `{table_name}`: {err.msg}")
        else:
            print(f"Таблица `{table_name}` успешно создана.")

    foreign_keys = []

    for fk_sql in foreign_keys:
        try:
            cursor.execute(fk_sql)
        except mysql.connector.Error as err:
            print(f"Ошибка при добавлении внешнего ключа: {err.msg}")
        else:
            print("Внешний ключ успешно добавлен.")

    # Добавление триггеров
    triggers = [
        """
        DELIMITER $$
        CREATE TRIGGER after_payment_insert
        AFTER INSERT ON payments
        FOR EACH ROW
        BEGIN
            DECLARE total_paid DECIMAL(15,2);

            -- Вычисляем общую сумму платежей по pledge_id
            SELECT SUM(amount) INTO total_paid
            FROM payments
            WHERE pledge_id = NEW.pledge_id;

            -- Получаем сумму кредита
            SELECT loan_amount INTO @loan_amount
            FROM pledges
            WHERE pledge_id = NEW.pledge_id;

            -- Обновляем статус, если сумма покрывает кредит
            IF total_paid >= @loan_amount THEN
                UPDATE pledges
                SET status = 'Выкуплен'
                WHERE pledge_id = NEW.pledge_id;
            ELSE
                UPDATE pledges
                SET status = 'Активный'
                WHERE pledge_id = NEW.pledge_id AND status != 'Продан';
            END IF;
        END$$
        DELIMITER ;
        """
    ]

    for trigger_sql in triggers:
        try:
            cleaned_sql = trigger_sql.replace("DELIMITER $$", "").replace("DELIMITER ;", "").replace("$$", ";")
            cursor.execute(cleaned_sql, multi=True)
        except mysql.connector.Error as err:
            print(f"Ошибка при создании триггера: {err.msg}")
        else:
            print("Триггер успешно создан.")


def seed_data():
    # Типы металлов
    metal_types = ['Золото', 'Серебро', 'Платина', 'Палладий', 'Мельхиор', 'Алюминий', 'Бронза', 'Титан', 'Никель', 'Сталь']
    add_metal_type = "INSERT IGNORE INTO metal_types (type_name) VALUES (%s)"
    for mt in metal_types:
        cursor.execute(add_metal_type, (mt,))
    cnx.commit()
    print("Типы металлов добавлены")

    cursor.execute("SELECT metal_type_id, type_name FROM metal_types")
    metal_type_rows = cursor.fetchall()
    metal_type_ids = {name: mid for mid, name in metal_type_rows}

    # Типы вставок
    inlay_types = ['Бриллиант', 'Рубин', 'Сапфир', 'Изумруд', 'Топаз', 'Аметист', 'Жемчуг', 'Опал', 'Гранат', 'Кварц']
    add_inlay_type = "INSERT IGNORE INTO inlay_types (type_name) VALUES (%s)"
    for it in inlay_types:
        cursor.execute(add_inlay_type, (it,))
    cnx.commit()
    print("Типы вставок добавлены")

    cursor.execute("SELECT inlay_type_id, type_name FROM inlay_types")
    inlay_type_rows = cursor.fetchall()
    inlay_type_ids = {name: iid for iid, name in inlay_type_rows}

    # Клиенты
    clients = [
        ('Иванов', 'Иван', 'Иванович', '1985-03-12', '4500', '123456', 'УВД ЦАО', '2010-07-20', 'ул. Ленина 10', 'ул. Пушкина 5', 9876543210, 'ivanov@example.com'),
        ('Петров', 'Петр', 'Петрович', '1990-08-22', '4501', '234567', 'УВД САО', '2011-01-14', 'ул. Гагарина 15', 'ул. Мира 30', 9876543211, 'petrov@example.com'),
        ('Сидоров', 'Александр', 'Николаевич', '1975-05-01', '4502', '345678', 'УВД ЗАО', '2012-03-10', 'ул. Тверская 5', 'ул. Арбат 10', 9876543212, 'sidorov@example.com'),
        ('Кузнецов', 'Дмитрий', 'Сергеевич', '1988-11-17', '4503', '456789', 'УВД ЮАО', '2013-09-05', 'ул. Кирова 8', 'ул. Ломоносова 12', 9876543213, 'kuznetsov@example.com'),
        ('Смирнова', 'Ольга', 'Владимировна', '1992-06-25', '4504', '567890', 'УВД ВАО', '2014-02-28', 'ул. Чехова 3', 'ул. Тургенева 7', 9876543214, 'smirnova@example.com'),
        ('Попова', 'Наталья', 'Алексеевна', '1980-01-10', '4505', '678901', 'УВД СЗАО', '2015-06-12', 'ул. Карла Маркса 14', 'ул. Ленина 20', 9876543215, 'popova@example.com'),
        ('Васильев', 'Алексей', 'Михайлович', '1995-09-30', '4506', '789012', 'УВД ЮЗАО', '2016-11-18', 'ул. Пушкина 10', 'ул. Лермонтова 5', 9876543216, 'vasilev@example.com'),
        ('Антонова', 'Елена', 'Петровна', '1983-04-05', '4507', '890123', 'УВД ЦАО', '2017-05-01', 'ул. Садовая 25', 'ул. Большая Никитская 1', 9876543217, 'antonova@example.com'),
        ('Михайлов', 'Сергей', 'Васильевич', '1979-12-19', '4508', '901234', 'УВД САО', '2018-08-23', 'ул. Красная 50', 'ул. Советская 15', 9876543218, 'mikhailov@example.com'),
        ('Фёдорова', 'Татьяна', 'Дмитриевна', '1993-02-14', '4509', '012345', 'УВД ЗАО', '2019-10-09', 'ул. Московская 100', 'ул. Санкт-Петербургская 20', 9876543219, 'fedorova@example.com')
    ]
    add_client = """
    INSERT IGNORE INTO clients (
        surname, name, patronymic, birth_date, passport_series, passport_number,
        passport_issued_by, passport_issue_date, residence_address, registration_address,
        phone, email
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for client in clients:
        cursor.execute(add_client, client)
    cnx.commit()
    print("Клиенты добавлены")

    cursor.execute("SELECT client_id FROM clients")
    client_ids = [row[0] for row in cursor.fetchall()]

    # Ценности
    descriptions = ["Кольцо с бриллиантом", "Серебряный браслет", "Позолоченная цепочка", "Часы Rolex",
                    "Золотой крестик", "Серьги с изумрудами", "Ложка из серебра", "Монета 19 века",
                    "Перстень с гранатом", "Золотая подвеска"]
    add_valuable = """
    INSERT INTO valuables (
        client_id, metal_type_id, inlay_type_id, weight, purity, description, appraised_value, received_date, storage_location
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for i in range(10):
        client_id = random.choice(client_ids)
        metal_type_id = random.choice(list(metal_type_ids.values()))
        inlay_type_id = random.choice(list(inlay_type_ids.values()))
        weight = round(random.uniform(1.0, 50.0), 3)
        purity = round(random.uniform(0.5, 0.999), 2)
        description = descriptions[i]
        appraised_value = round(random.uniform(10000, 500000), 2)
        received_date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d')
        storage_location = f"Сейф #{i+1}"

        cursor.execute(add_valuable, (client_id, metal_type_id, inlay_type_id, weight, purity,
                                      description, appraised_value, received_date, storage_location))
    cnx.commit()
    print("Ценности добавлены")

    cursor.execute("SELECT valuable_id FROM valuables")
    valuable_ids = [row[0] for row in cursor.fetchall()]

    pawnshops = [
        ("Ломбард Центр", "ул. Ленина 1", "+7 495 123-45-67", "center@pawnshop.ru", "09:00 - 18:00"),
        ("Ломбард Север", "ул. Лесная 10", "+7 495 987-65-43", "north@pawnshop.ru", "10:00 - 20:00"),
        ("Ломбард Юг", "ул. Теплая 5", "+7 495 111-22-33", "south@pawnshop.ru", "08:00 - 17:00"),
        ("Ломбард Восток", "ул. Уральская 20", "+7 495 444-55-66", "east@pawnshop.ru", "11:00 - 19:00"),
        ("Ломбард Запад", "ул. Октябрьская 15", "+7 495 777-88-99", "west@pawnshop.ru", "09:00 - 21:00"),
        ("Русский Ломбард", "ул. Пушкина 3", "+7 495 222-33-44", "russian@pawnshop.ru", "09:00 - 18:00"),
        ("Золотой Запас", "ул. Золотая 1", "+7 495 555-66-77", "gold@pawnshop.ru", "10:00 - 19:00"),
        ("Столичный Ломбард", "ул. Тверская 5", "+7 495 888-99-00", "capital@pawnshop.ru", "09:00 - 20:00"),
        ("Автоломбард", "ул. Автомобильная 10", "+7 495 333-44-55", "auto@pawnshop.ru", "08:00 - 18:00"),
        ("Ювелирный Ломбард", "ул. Белинского 12", "+7 495 666-77-88", "jewelry@pawnshop.ru", "10:00 - 18:00")
    ]
    add_pawnshop = """
    INSERT INTO pawnshops (name, address, phone, email, working_hours) 
    VALUES (%s, %s, %s, %s, %s)
    """
    for p in pawnshops:
        cursor.execute(add_pawnshop, p)
    cnx.commit()
    print("Ломбарды добавлены")

    cursor.execute("SELECT pawnshop_id FROM pawnshops")
    pawnshop_ids = [row[0] for row in cursor.fetchall()]

    positions = ["Менеджер", "Кассир", "Оценщик", "Администратор"]
    add_employee = """
    INSERT INTO employees (pawnshop_id, surname, name, patronymic, position, phone, email, hire_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    for i in range(10):
        pawnshop_id = random.choice(pawnshop_ids)
        surname = f"Сотрудник{i}"
        name = f"Имя{i}"
        patronymic = f"Отчество{i}"
        position = random.choice(positions)
        phone = f"+7 999 123-45-{i:02d}"
        email = f"employee{i}@pawnshop.ru"
        hire_date = (datetime.now() - timedelta(days=random.randint(30, 1000))).strftime('%Y-%m-%d')
        cursor.execute(add_employee, (pawnshop_id, surname, name, patronymic, position, phone, email, hire_date))
    cnx.commit()
    print("Сотрудники добавлены")

    cursor.execute("SELECT employee_id FROM employees")
    employee_ids = [row[0] for row in cursor.fetchall()]

    # Залоги
    statuses = ['Активный', 'Выкуплен', 'Продан']
    add_pledge = """
    INSERT INTO pledges (
        valuable_id, pawnshop_id, employee_id, pledge_date, end_date, loan_amount, interest_rate, status, comments
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for i in range(10):
        valuable_id = random.choice(valuable_ids)
        pawnshop_id = random.choice(pawnshop_ids)
        employee_id = random.choice(employee_ids)
        pledge_date = (datetime.now() - timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d')
        end_date = (datetime.now() + timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d')
        loan_amount = round(random.uniform(10000, 500000), 2)
        interest_rate = round(random.uniform(1.0, 10.0), 2)
        status = random.choice(statuses)
        comment = f"Комментарий к залогу #{i}"

        cursor.execute(add_pledge, (valuable_id, pawnshop_id, employee_id, pledge_date, end_date,
                                    loan_amount, interest_rate, status, comment))
    cnx.commit()
    print("Залоги добавлены")

    cursor.execute("SELECT pledge_id FROM pledges")
    pledge_ids = [row[0] for row in cursor.fetchall()]

    # Платежи
    payment_types = ['Частичная выплата', 'Полный выкуп']
    add_payment = """
    INSERT INTO payments (pledge_id, employee_id, payment_date, amount, payment_type, comments)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    for i in range(10):
        pledge_id = random.choice(pledge_ids)
        employee_id = random.choice(employee_ids)
        payment_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
        amount = round(random.uniform(1000, 300000), 2)
        payment_type = random.choice(payment_types)
        comment = f"Платёж #{i}"

        cursor.execute(add_payment, (pledge_id, employee_id, payment_date, amount, payment_type, comment))
    cnx.commit()
    print("Платежи добавлены")


def run_sample_queries(cursor):
    queries = [
    ]

    for q in queries:
        print(f"\n--- {q['description']} ---")
        try:
            cursor.execute(q['sql'])
            results = cursor.fetchall()
            if results:
                print(tabulate(results, headers=[desc[0] for desc in cursor.description], tablefmt="grid"))
            else:
                print("Нет данных.")
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")


def describe_table(table_name):
    """
    Выводит структуру таблицы в формате DESCRIBE из MySQL
    """
    query = f"""
    SELECT 
        COLUMN_NAME AS `Field`,
        COLUMN_TYPE AS `Type`,
        IS_NULLABLE AS `Null`,
        CASE 
            WHEN COLUMN_KEY = 'PRI' THEN 'PRI'
            WHEN COLUMN_KEY = 'UNI' THEN 'UNI'
            WHEN COLUMN_KEY = 'MUL' THEN 'MUL'
            ELSE '' 
        END AS `Key`,
        COLUMN_DEFAULT AS `Default`,
        EXTRA AS Extra
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
    ORDER BY ORDINAL_POSITION;
    """

    try:
        cursor.execute(query, (cnx.database, table_name))
        result = cursor.fetchall()

        if not result:
            print(f"Таблица `{table_name}` не найдена или пуста.")
            return

        headers = ["Field", "Type", "Null", "Key", "Default", "Extra"]
        print(tabulate(result, headers=headers, tablefmt="grid"))

    except mysql.connector.Error as err:
        print(f"Ошибка при описании таблицы `{table_name}`: {err}")


if __name__ == '__main__':
    # create_tables()
    seed_data()
