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

    # Добавление сообщений
    add_message = ("INSERT INTO messages "
                   "(text, chat_id, user_id) VALUES (%s, %s, %s)")
    cursor.execute(add_message, ("Привет всем!", chat_ids[0], user_ids['alice']))
    cursor.execute(add_message, ("Как дела?", chat_ids[0], user_ids['bob']))
    cursor.execute(add_message, ("Работаем над задачами", chat_ids[1], user_ids['alice']))
    cnx.commit()

    # Токены обновления
    add_refresh_token = ("INSERT INTO refresh_tokens "
                         "(token_id, user_id, token, expires_at) VALUES (%s, %s, %s, %s)")
    for username in user_ids:
        token_id = str(uuid.uuid4())
        token = str(uuid.uuid4())
        expires = datetime.now() + timedelta(days=30)
        cursor.execute(add_refresh_token, (token_id, user_ids[username], token, expires))
    cnx.commit()

    # Asset-токены
    add_asset_token = ("INSERT INTO asset_tokens "
                       "(token_id, asset_url, expires_at) VALUES (%s, %s, %s)")
    for i in range(2):
        cursor.execute(add_asset_token, (
            str(uuid.uuid4()),
            f"https://example.com/assets/sample{i}.jpg",
            datetime.now() + timedelta(hours=1)
        ))
    cnx.commit()

    # Ключи шифрования
    add_key = ("INSERT INTO encryption_keys "
               "(user_id, public_key, private_key_encrypted, fingerprint) VALUES (%s, %s, %s, %s)")
    for username in ['alice', 'bob']:
        cursor.execute(add_key, (
            user_ids[username],
            f"public_key_of_{username}",
            f"encrypted_private_key_of_{username}",
            f"fingerprint_{uuid.uuid4().hex[:16]}"
        ))
    cnx.commit()
    print("Чаты и участники добавлены")


def run_sample_queries(cursor):
    queries = [
        {
            "description": "1. Все пользователи с последним статусом и временем последнего посещения",
            "sql": """
                SELECT username, status, last_seen
                FROM users
                ORDER BY last_seen DESC;
            """
        },
        {
            "description": "2. Список чатов с владельцами и количеством участников",
            "sql": """
                SELECT c.title, u.username AS owner, COUNT(cp.user_id) AS participants
                FROM chats c
                JOIN users u ON c.owner_id = u.user_id
                LEFT JOIN chat_participants cp ON c.chat_id = cp.chat_id
                GROUP BY c.chat_id;
            """
        },
        {
            "description": "3. Сообщения из чата с ID = 1 с именами авторов",
            "sql": """
                SELECT m.text, m.created_at, u.username
                FROM messages m
                JOIN users u ON m.user_id = u.user_id
                WHERE m.chat_id = 1
                ORDER BY m.created_at ASC;
            """
        },
        {
            "description": "4. Чаты, в которых состоит пользователь 'alice'",
            "sql": """
                SELECT c.title, cp.role
                FROM chat_participants cp
                JOIN chats c ON cp.chat_id = c.chat_id
                WHERE cp.user_id = (SELECT user_id FROM users WHERE username = 'alice');
            """
        },
        {
            "description": "5. Пользователи без участия в чатах",
            "sql": """
                SELECT u.username
                FROM users u
                LEFT JOIN chat_participants cp ON u.user_id = cp.user_id
                WHERE cp.chat_id IS NULL;
            """
        },
        {
            "description": "6. Изменённые сообщения пользователя 'bob'",
            "sql": """
                SELECT m.text, m.updated_at
                FROM messages m
                JOIN users u ON m.user_id = u.user_id
                WHERE u.username = 'bob' AND m.is_edited = TRUE;
            """
        },
        {
            "description": "7. Активные refresh-токены",
            "sql": """
                SELECT token_id, user_id, expires_at
                FROM refresh_tokens
                WHERE revoked = FALSE AND expires_at > NOW();
            """
        },
        {
            "description": "8. Публичные чаты типа 'CHANNEL'",
            "sql": """
                SELECT title, description
                FROM chats
                WHERE is_public = TRUE AND type = 'CHANNEL';
            """
        },
        {
            "description": "9. Участники с ролью 'ADMIN' или 'OWNER'",
            "sql": """
                SELECT u.username, c.title, cp.role
                FROM chat_participants cp
                JOIN users u ON cp.user_id = u.user_id
                JOIN chats c ON cp.chat_id = c.chat_id
                WHERE cp.role IN ('ADMIN', 'OWNER');
            """
        },
        {
            "description": "10. Сообщения с прикреплёнными файлами",
            "sql": """
                SELECT m.message_id, m.attachment_url, m.attachment_type
                FROM messages m
                WHERE m.attachment_url IS NOT NULL;
            """
        }
    ]

    for q in queries:
        print(f"\n--- {q['description']} ---")
        try:
            cursor.execute(q['sql'])
            results = cursor.fetchall()
            if results:
                print(tabulate(results, headers=[i[0] for i in cursor.description], tablefmt="grid"))
            else:
                print("Нет данных.")
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")


if __name__ == '__main__':
    create_tables()
    seed_data()

    run_sample_queries(cursor)
    # table_to_describe = "messages"
    # print(f"\n--- Структура таблицы `{table_to_describe}` ---")
    # describe_table(table_to_describe)

    cursor.close()
    cnx.close()
