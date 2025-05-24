import mysql.connector
from mysql.connector import errorcode
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
      delivered_to JSON DEFAULT ('[]'),
      read_by JSON DEFAULT ('[]'),
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

    # Создание индексов
    INDEXES = [
        "CREATE INDEX idx_chats_title ON chats(title)",
        "CREATE UNIQUE INDEX chat_participants_index_1 ON chat_participants(user_id, chat_id)",
        "CREATE INDEX idx_messages_chatid_createdat ON messages(chat_id, created_at)"
    ]

    for table_name in TABLES:
        table_sql = TABLES[table_name]
        try:
            print(f"Создается таблица {table_name}...")
            cursor.execute(table_sql)
        except mysql.connector.Error as err:
            print(f"Ошибка при создании таблицы {table_name}: {err.msg}")

    for index_sql in INDEXES:
        try:
            cursor.execute(index_sql)
        except mysql.connector.Error as err:
            print(f"Ошибка при создании индекса: {err.msg}")

    print("Все таблицы и индексы созданы")

def seed_data():
    add_user = ("INSERT INTO users "
                "(username, email, password_hash, avatar_url, status, last_seen) "
                "VALUES (%s, %s, %s, %s, %s, NOW())")

    users = [
        ('alice', 'alice@example.com', 'hash123', 'https://example.com/avatars/alice.jpg ', 'online'),
        ('bob', 'bob@example.com', 'hash456', 'https://example.com/avatars/bob.jpg ', 'away')
    ]

    for user in users:
        cursor.execute(add_user, user)
    cnx.commit()

    add_chat = ("INSERT INTO chats "
                "(title, description, type, is_public, owner_id) "
                "VALUES (%s, %s, %s, %s, %s)")

    chat_data = ('Чат друзей', 'Общий чат для друзей', 'GROUP', True, 1)
    cursor.execute(add_chat, chat_data)
    chat_id = cursor.lastrowid

    add_participant = ("INSERT INTO chat_participants "
                       "(user_id, chat_id, role) VALUES (%s, %s, %s)")
    cursor.execute(add_participant, (1, chat_id, 'OWNER'))
    cursor.execute(add_participant, (2, chat_id, 'MEMBER'))

    cnx.commit()

    print("Тестовые данные добавлены")


def seed_data():
    # Добавляем пользователей
    add_user = ("INSERT INTO users "
                "(username, email, password_hash, avatar_url, status, last_seen) "
                "VALUES (%s, %s, %s, %s, %s, NOW())")

    users = [
        ('alice', 'alice@example.com', 'hash123', 'https://example.com/avatars/alice.jpg ', 'online'),
        ('bob', 'bob@example.com', 'hash456', 'https://example.com/avatars/bob.jpg ', 'away')
    ]

    for user in users:
        cursor.execute(add_user, user)
    cnx.commit()

    # Создаем чат
    add_chat = ("INSERT INTO chats "
                "(title, description, type, is_public, owner_id) "
                "VALUES (%s, %s, %s, %s, %s)")

    chat_data = ('Чат друзей', 'Общий чат для друзей', 'GROUP', True, 1)
    cursor.execute(add_chat, chat_data)
    chat_id = cursor.lastrowid

    # Добавляем участников
    add_participant = ("INSERT INTO chat_participants "
                       "(user_id, chat_id, role) VALUES (%s, %s, %s)")
    cursor.execute(add_participant, (1, chat_id, 'OWNER'))
    cursor.execute(add_participant, (2, chat_id, 'MEMBER'))

    cnx.commit()

    print("Тестовые данные добавлены")


def get_all_users():
    """
    Получить всех пользователей
    """
    cursor.execute("SELECT username, email FROM users")
    result = cursor.fetchall()
    for row in result:
        print(row)


def get_user_chats(user_id):
    """
    Получить чаты пользователя
    Args:
        user_id:
    """
    query = """
    SELECT c.title, c.type 
    FROM chat_participants cp
    JOIN chats c ON cp.chat_id = c.chat_id
    WHERE cp.user_id = %s AND cp.left_at IS NULL
    """
    cursor.execute(query, (user_id,))
    result = cursor.fetchall()
    for row in result:
        print(row)


def send_message(chat_id, user_id, text):
    """
    Отправить сообщение
    Args:
        chat_id:
        user_id:
        text:
    """
    insert = """
    INSERT INTO messages (text, chat_id, user_id)
    VALUES (%s, %s, %s)
    """
    cursor.execute(insert, (text, chat_id, user_id))
    cnx.commit()
    print("Сообщение отправлено")


if __name__ == '__main__':
    create_tables()
    seed_data()

    print("\n--- Все пользователи ---")
    get_all_users()

    print("\n--- Чаты пользователя ID=1 ---")
    get_user_chats(1)

    print("\n--- Отправка сообщения ---")
    send_message(chat_id=1, user_id=1, text="Привет")

    cursor.close()
    cnx.close()