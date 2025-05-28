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

    # Добавление внешних ключей (оставляем пустым, так как они уже добавлены в CREATE TABLE)
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
    cnx.commit()


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
    create_tables()
