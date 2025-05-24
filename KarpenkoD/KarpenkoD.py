import mysql.connector
from mysql.connector import errorcode
from tabulate import tabulate
import uuid
from datetime import datetime, timedelta

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'messenger_db',
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

    TABLES['users'] = """
    CREATE TABLE IF NOT EXISTS users (
      user_id INT PRIMARY KEY AUTO_INCREMENT,
      username VARCHAR(50) UNIQUE NOT NULL,
      email VARCHAR(100) UNIQUE NOT NULL,
      password_hash TEXT NOT NULL,
      avatar_url VARCHAR(255),
      status ENUM ('online', 'offline', 'away'),
      last_seen DATETIME,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB;
    """

    TABLES['chats'] = """
    CREATE TABLE IF NOT EXISTS chats (
      chat_id INT PRIMARY KEY AUTO_INCREMENT,
      title VARCHAR(100),
      description TEXT,
      avatar_url VARCHAR(255),
      type ENUM ('PRIVATE', 'GROUP', 'CHANNEL') NOT NULL,
      is_public BOOLEAN DEFAULT false,
      owner_id INT,
      settings JSON,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (owner_id) REFERENCES users(user_id)
    ) ENGINE=InnoDB;
    """

    TABLES['chat_participants'] = """
    CREATE TABLE IF NOT EXISTS chat_participants (
      participant_id INT PRIMARY KEY AUTO_INCREMENT,
      user_id INT NOT NULL,
      chat_id INT NOT NULL,
      role ENUM ('OWNER', 'ADMIN', 'MEMBER') DEFAULT 'MEMBER',
      joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      left_at DATETIME DEFAULT NULL,
      is_muted BOOLEAN DEFAULT false,
      FOREIGN KEY (user_id) REFERENCES users(user_id),
      FOREIGN KEY (chat_id) REFERENCES chats(chat_id)
    ) ENGINE=InnoDB;
    """

    TABLES['messages'] = """
    CREATE TABLE IF NOT EXISTS messages (
      message_id INT PRIMARY KEY AUTO_INCREMENT,
      text TEXT,
      attachment_url VARCHAR(255),
      attachment_type VARCHAR(50),
      metadata JSON,
      is_edited BOOLEAN DEFAULT false,
      is_deleted BOOLEAN DEFAULT false,
      reply_to_id INT DEFAULT null,
      reactions JSON,
      delivered_to JSON,
      read_by JSON,
      chat_id INT NOT NULL,
      user_id INT NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (chat_id) REFERENCES chats(chat_id),
      FOREIGN KEY (user_id) REFERENCES users(user_id),
      FOREIGN KEY (reply_to_id) REFERENCES messages(message_id)
    ) ENGINE=InnoDB;
    """

    TABLES['asset_tokens'] = """
    CREATE TABLE IF NOT EXISTS asset_tokens (
      token_id CHAR(36) PRIMARY KEY,
      asset_url VARCHAR(255) NOT NULL,
      expires_at DATETIME NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB;
    """

    TABLES['refresh_tokens'] = """
    CREATE TABLE IF NOT EXISTS refresh_tokens (
      token_id CHAR(36) PRIMARY KEY,
      user_id INT NOT NULL,
      token TEXT NOT NULL,
      expires_at DATETIME NOT NULL,
      revoked BOOLEAN DEFAULT false,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(user_id)
    ) ENGINE=InnoDB;
    """

    TABLES['encryption_keys'] = """
    CREATE TABLE IF NOT EXISTS encryption_keys (
      key_id INT PRIMARY KEY AUTO_INCREMENT,
      user_id INT NOT NULL,
      public_key TEXT NOT NULL,
      private_key_encrypted TEXT NOT NULL,
      fingerprint VARCHAR(64) NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(user_id)
    ) ENGINE=InnoDB;
    """

    for table_name in TABLES:
        table_sql = TABLES[table_name]
        try:
            print(f"CREATE TABLE {table_name};")
            cursor.execute(table_sql)
        except mysql.connector.Error as err:
            print(f"Ошибка при создании таблицы `{table_name}`: {err.msg}")

    # Индексы тоже выводим
    INDEXES = [
        "CREATE INDEX idx_chats_title ON chats(title)",
        "CREATE UNIQUE INDEX chat_participants_index_1 ON chat_participants(user_id, chat_id)",
        "CREATE INDEX idx_messages_chatid_createdat ON messages(chat_id, created_at)"
    ]

    for index_sql in INDEXES:
        try:
            print(f"{index_sql};")
            cursor.execute(index_sql)
        except mysql.connector.Error as err:
            print(f"Ошибка при создании индекса: {err.msg}")

print("Все таблицы и индексы созданы")


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


def seed_data():
    add_user = ("INSERT IGNORE INTO users "
                "(username, email, password_hash, avatar_url, status, last_seen) "
                "VALUES (%s, %s, %s, %s, %s, NOW())")
    users = [
        ('alice', 'alice@example.com', 'hash123', 'https://example.com/avatars/alice.jpg', 'online'),
        ('bob', 'bob@example.com', 'hash456', 'https://example.com/avatars/bob.jpg', 'away'),
        ('charlie', 'charlie@example.com', 'hash789', 'https://example.com/avatars/charlie.jpg', 'offline'),
        ('diana', 'diana@example.com', 'hash000', 'https://example.com/avatars/diana.jpg', 'online')
    ]
    for user in users:
        cursor.execute(add_user, user)
    cnx.commit()
    print("Пользователи добавлены")

    # user_id для 'alice'
    cursor.execute("SELECT user_id FROM users WHERE username = 'alice'")
    result = cursor.fetchone()
    if not result:
        print("Ошибка: пользователь 'alice' не найден!")
        return
    owner_id = result[0]

    # Создание чатов
    add_chat = ("INSERT INTO chats "
                "(title, description, type, is_public, owner_id) "
                "VALUES (%s, %s, %s, %s, %s)")

    chats = [
        ('Чат друзей', 'Общий чат для друзей', 'GROUP', True, owner_id),
        ('Рабочий чат', 'Командная работа', 'GROUP', False, owner_id),
        ('Техническая поддержка', 'Вопросы и ответы', 'CHANNEL', True, owner_id)
    ]

    chat_ids = []
    for chat_data in chats:
        cursor.execute(add_chat, chat_data)
        chat_ids.append(cursor.lastrowid)

    # Добавление участников в первый чат
    add_participant = ("INSERT INTO chat_participants "
                       "(user_id, chat_id, role) VALUES (%s, %s, %s)")

    # id всех пользователей
    cursor.execute("SELECT user_id, username FROM users")
    user_rows = cursor.fetchall()
    user_ids = {username: user_id for user_id, username in user_rows}

    # Добавление участников
    cursor.execute(add_participant, (user_ids['alice'], chat_ids[0], 'OWNER'))
    cursor.execute(add_participant, (user_ids['bob'], chat_ids[0], 'MEMBER'))
    cursor.execute(add_participant, (user_ids['charlie'], chat_ids[0], 'MEMBER'))

    cursor.execute(add_participant, (user_ids['alice'], chat_ids[1], 'OWNER'))
    cursor.execute(add_participant, (user_ids['diana'], chat_ids[1], 'MEMBER'))

    cursor.execute(add_participant, (user_ids['alice'], chat_ids[2], 'OWNER'))

    cnx.commit()
    print("Чаты и участники добавлены")



if __name__ == '__main__':
    create_tables()
    seed_data()

    # table_to_describe = "messages"
    # print(f"\n--- Структура таблицы `{table_to_describe}` ---")
    # describe_table(table_to_describe)

    cursor.close()
    cnx.close()
