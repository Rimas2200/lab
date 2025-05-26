import mysql.connector
from mysql.connector import errorcode
from tabulate import tabulate
import uuid
from datetime import datetime, timedelta

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


    for table_name in TABLES:
        table_sql = TABLES[table_name]
        try:
            print(f"CREATE TABLE {table_name};")
            cursor.execute(table_sql)
        except mysql.connector.Error as err:
            print(f"Ошибка при создании таблицы `{table_name}`: {err.msg}")


if __name__ == '__main__':
    create_tables()