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
    'database': '',
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

    TABLES['___'] = """
    CREATE TABLE IF NOT EXISTS ___ (
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
