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
    'database': 'car_db',
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

    TABLES['clients'] = """
    CREATE TABLE IF NOT EXISTS clients(
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

    TABLES['car_brands'] = """
    CREATE TABLE IF NOT EXISTS car_brands (
      brand_id INT PRIMARY KEY AUTO_INCREMENT,
      brand_name VARCHAR(50) UNIQUE NOT NULL
    ) ENGINE=InnoDB;
    """

    TABLES['cars'] = """
    CREATE TABLE IF NOT EXISTS cars (
      car_id INT PRIMARY KEY AUTO_INCREMENT,
      client_id INT,
      brand_id INT,                         
      model VARCHAR(50),
      year INT,
      vin VARCHAR(17) UNIQUE,
      license_plate VARCHAR(15),
      technical_passport VARCHAR(50),
      color VARCHAR(30),
      engine_capacity DECIMAL(5,2),
      fuel_type ENUM ('Бензин', 'Дизель', 'Электро', 'Гибрид'),
      mileage INT
    ) ENGINE=InnoDB;
    """

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
      hire_date DATE
    ) ENGINE=InnoDB;
    """

    TABLES['pledges'] = """
    CREATE TABLE IF NOT EXISTS pledges (
      pledge_id INT PRIMARY KEY AUTO_INCREMENT,
      car_id INT,
      pawnshop_id INT,
      employee_id INT,
      pledge_date DATE,
      end_date DATE,
      amount DECIMAL(15,2),
      interest_rate DECIMAL(5,2),
      status ENUM ('Активный', 'Выкуплен', 'Продан') DEFAULT 'Активный',
      comments TEXT
    ) ENGINE=InnoDB;
    """

    TABLES['payments'] = """
    CREATE TABLE IF NOT EXISTS payments (
      payment_id INT PRIMARY KEY AUTO_INCREMENT,
      pledge_id INT,
      employee_id INT,
      payment_date DATE,
      amount DECIMAL(15,2),
      payment_type ENUM ('Частичная выплата', 'Полный выкуп'),
      comments TEXT
    ) ENGINE=InnoDB;
    """

    TABLES['sold_cars'] = """
    CREATE TABLE IF NOT EXISTS sold_cars (
      sold_id INT PRIMARY KEY AUTO_INCREMENT,
      client_id INT,
      car_id INT,
      pledge_amount DECIMAL(15,2),
      sold_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB;
    """

    TABLES['redeemed_cars'] = """
    CREATE TABLE IF NOT EXISTS redeemed_cars (
      redeemed_id INT PRIMARY KEY AUTO_INCREMENT,
      client_id INT,
      car_id INT,
      pledge_amount DECIMAL(15,2),
      redeemed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

    # Добавление внешних ключей
    foreign_keys = [
        "ALTER TABLE cars ADD FOREIGN KEY (client_id) REFERENCES clients(client_id);",
        "ALTER TABLE cars ADD FOREIGN KEY (brand_id) REFERENCES car_brands(brand_id);",

        "ALTER TABLE employees ADD FOREIGN KEY (pawnshop_id) REFERENCES pawnshops(pawnshop_id);",

        "ALTER TABLE pledges ADD FOREIGN KEY (car_id) REFERENCES cars(car_id);",
        "ALTER TABLE pledges ADD FOREIGN KEY (pawnshop_id) REFERENCES pawnshops(pawnshop_id);",
        "ALTER TABLE pledges ADD FOREIGN KEY (employee_id) REFERENCES employees(employee_id);",

        "ALTER TABLE payments ADD FOREIGN KEY (pledge_id) REFERENCES pledges(pledge_id);",
        "ALTER TABLE payments ADD FOREIGN KEY (employee_id) REFERENCES employees(employee_id);",

        "ALTER TABLE sold_cars ADD FOREIGN KEY (client_id) REFERENCES clients(client_id);",
        "ALTER TABLE sold_cars ADD FOREIGN KEY (car_id) REFERENCES cars(car_id);",

        "ALTER TABLE redeemed_cars ADD FOREIGN KEY (client_id) REFERENCES clients(client_id);",
        "ALTER TABLE redeemed_cars ADD FOREIGN KEY (car_id) REFERENCES cars(car_id);"
    ]

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
        CREATE TRIGGER after_pledge_status_update_sold
        AFTER UPDATE ON pledges
        FOR EACH ROW
        BEGIN
          IF NEW.status = 'Продан' AND OLD.status != 'Продан' THEN
            INSERT INTO sold_cars (client_id, car_id, pledge_amount)
            VALUES (
              (SELECT client_id FROM cars WHERE car_id = NEW.car_id),
              NEW.car_id,
              NEW.amount
            );
          END IF;
        END$$
        """,
        """
        DELIMITER $$
        CREATE TRIGGER after_pledge_status_update_redeemed
        AFTER UPDATE ON pledges
        FOR EACH ROW
        BEGIN
          IF NEW.status = 'Выкуплен' AND OLD.status != 'Выкуплен' THEN
            INSERT INTO redeemed_cars (client_id, car_id, pledge_amount)
            VALUES (
              (SELECT client_id FROM cars WHERE car_id = NEW.car_id),
              NEW.car_id,
              NEW.amount
            );
          END IF;
        END$$
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
    car_brands = ['Toyota', 'BMW', 'Mercedes', 'Ford', 'Honda', 'Volkswagen', 'Audi', 'Hyundai', 'Kia', 'Lexus']
    add_brand = "INSERT IGNORE INTO car_brands (brand_name) VALUES (%s)"
    for brand in car_brands:
        cursor.execute(add_brand, (brand,))
    cnx.commit()
    print("Бренды автомобилей добавлены")

    cursor.execute("SELECT brand_id, brand_name FROM car_brands")
    brand_rows = cursor.fetchall()
    brand_ids = {name: bid for bid, name in brand_rows}

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

    cursor.execute("SELECT client_id, surname FROM clients")
    client_rows = cursor.fetchall()
    client_ids = {surname: cid for cid, surname in client_rows}

    models = ['Camry', 'Corolla', 'Civic', 'Accord', 'Passat', 'Golf', '3 Series', '5 Series', 'C-Class', 'F-150']
    colors = ['Чёрный', 'Белый', 'Серебристый', 'Красный', 'Синий']
    fuels = ['Бензин', 'Дизель', 'Электро', 'Гибрид']

    add_car = """
    INSERT INTO cars (
        client_id, brand_id, model, year, vin, license_plate,
        technical_passport, color, engine_capacity, fuel_type, mileage
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for i in range(10):
        client_id = random.choice(list(client_ids.values()))
        brand_id = random.choice(list(brand_ids.values()))
        model = models[i % len(models)]
        year = random.randint(2010, 2023)
        vin = f"VIN{i}{uuid.uuid4().hex[:12]}"
        license_plate = f"A{i}BC{random.randint(100, 999)}RU"
        tech_passport = f"TP-{i}-{uuid.uuid4().hex[:8]}"
        color = random.choice(colors)
        engine = round(random.uniform(1.0, 5.0), 1)
        fuel = random.choice(fuels)
        mileage = random.randint(1000, 200000)

        cursor.execute(add_car, (client_id, brand_id, model, year, vin, license_plate,
                                 tech_passport, color, engine, fuel, mileage))
    cnx.commit()
    print("Автомобили добавлены")

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

    # Получаем pawnshop_id
    cursor.execute("SELECT pawnshop_id, name FROM pawnshops")
    pawnshop_rows = cursor.fetchall()
    pawnshop_ids = {name: pid for pid, name in pawnshop_rows}

    positions = ["Менеджер", "Кассир", "Оценщик", "Администратор"]
    add_employee = """
    INSERT INTO employees (pawnshop_id, surname, name, patronymic, position, phone, email, hire_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    for i in range(10):
        pawnshop_id = random.choice(list(pawnshop_ids.values()))
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

    cursor.execute("SELECT car_id FROM cars")
    car_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT pawnshop_id FROM pawnshops")
    pawnshop_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT employee_id FROM employees")
    employee_ids = [row[0] for row in cursor.fetchall()]

    statuses = ['Активный', 'Выкуплен', 'Продан']
    add_pledge = """
    INSERT INTO pledges (
        car_id, pawnshop_id, employee_id, pledge_date, end_date, amount, interest_rate, status, comments
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for i in range(10):
        car_id = random.choice(car_ids)
        pawnshop_id = random.choice(pawnshop_ids)
        employee_id = random.choice(employee_ids)
        pledge_date = (datetime.now() - timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d')
        end_date = (datetime.now() + timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d')
        amount = round(random.uniform(100000, 1000000), 2)
        interest_rate = round(random.uniform(1.0, 10.0), 2)
        status = random.choice(statuses)
        comment = f"Комментарий к залогу #{i}"

        cursor.execute(add_pledge, (car_id, pawnshop_id, employee_id, pledge_date, end_date,
                                    amount, interest_rate, status, comment))
    cnx.commit()
    print("Залоги добавлены")

    payment_types = ['Частичная выплата', 'Полный выкуп']
    cursor.execute("SELECT pledge_id FROM pledges")
    pledge_ids = [row[0] for row in cursor.fetchall()]

    add_payment = """
    INSERT INTO payments (pledge_id, employee_id, payment_date, amount, payment_type, comments)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    for i in range(10):
        pledge_id = random.choice(pledge_ids)
        employee_id = random.choice(employee_ids)
        payment_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
        amount = round(random.uniform(10000, 500000), 2)
        payment_type = random.choice(payment_types)
        comment = f"Платёж #{i}"

        cursor.execute(add_payment, (pledge_id, employee_id, payment_date, amount, payment_type, comment))
    cnx.commit()


if __name__ == '__main__':
    # create_tables()
    seed_data()
