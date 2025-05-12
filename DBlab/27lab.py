import pprint
import sqlite3
connect = sqlite3.connect('bd_shop.sqlite')
cursor = connect.cursor()
pp = pprint.PrettyPrinter(indent=1, width=80, compact=False) 

# 1 Задание
cursor.execute('''Alter table prices rename to new_prices''')
pp.pprint(cursor.fetchall())
conn.commit()

cursor.execute('''select tbl_name, sql From sqlite_master''')
pp.pprint(cursor.fetchall())

# 2 Задание
cursor.execute('''ALTER TABLE customers ADD AGE int(2) constraint CK_customers_AGE check(AGE > 0 and AGE < 100) constraint DF_customers_AGE default(18)''')
cursor.execute('''ALTER TABLE customers ADD Phone varchar(20) constraint DF_customers_Phone default('no')''')
cursor.execute('''select tbl_name, sql From sqlite_master''')
pp.pprint(cursor.fetchall())
cursor.execute('''select * from customers''')
pp.pprint(cursor.fetchall())
connect.commit()

# 3 Задание
cursor.execute('''ALTER TABLE customers RENAME TO customers_old''')
connect.commit()
cursor.execute('''CREATE TABLE customers (
  id_customer INTEGER NOT NULL, 
  name char(50) NOT NULL,
  email char(50) NOT NULL,
  constraint PK_customers_id_customer PRIMARY KEY (id_customer),
  CONSTRAINT UQ_customers_EMAIL UNIQUE (email)
)''')
connect.commit()
cursor.execute('''INSERT INTO customers (id_customer, name, email)
SELECT id_customer, name, email
FROM customers_old;
''')
connect.commit()
cursor.execute('''DROP TABLE customers_old''')
connect.commit()
cursor.execute('''select * from customers''')
pp.pprint(cursor.fetchall())

# 4 Задание
cursor.execute('''ALTER TABLE magazine_sales RENAME TO magazine_sales_old''')
connect.commit()

cursor.execute('''create table magazine_sales (
  id_sale int NOT NULL,
  id_product int NOT NULL,
  N int NOT NULL,
  constraint PK_magazine_sales_id_sale_id_product PRIMARY KEY(id_sale, id_product),
  constraint FK_magazine_sales_id_sale FOREIGN KEY(id_sale) references sale(id_sale),
  constraint FK_magazine_sales_id_product FOREIGN KEY(id_product) references products(id_product),
  constraint CK_magazine_sales_quantity check(N>0)
  )''')
connect.commit()
cursor.execute('''INSERT INTO magazine_sales (id_sale, id_product, N)
SELECT id_sale, id_product, quantity
FROM magazine_sales_old;
''')
connect.commit()
cursor.execute('''DROP TABLE magazine_sales_old''')
connect.commit()

cursor.execute('''select tbl_name, sql From sqlite_master''')
pp.pprint(cursor.fetchall())

# 5 Задание
cursor.execute('''ALTER TABLE magazine_sales RENAME TO magazine_sales_old''')
connect.commit()
cursor.execute('''create table magazine_sales (
  id_sale int NOT NULL,
  id_product int NOT NULL,
  quantity int NOT NULL default(1),
  constraint PK_magazine_sales_id_sale_id_product PRIMARY KEY(id_sale, id_product),
  constraint FK_magazine_sales_id_sale FOREIGN KEY(id_sale) references sale(id_sale),
  constraint FK_magazine_sales_id_product FOREIGN KEY(id_product) references products(id_product),
  constraint CK_magazine_sales_quantity check(quantity>=0 and quantity<=10)
  )''')
connect.commit()
cursor.execute('''INSERT INTO magazine_sales (id_sale, id_product, quantity)
SELECT id_sale, id_product, quantity
FROM magazine_sales_old;
''')
connect.commit()
cursor.execute('''DROP TABLE magazine_sales_old''')
connect.commit()

cursor.execute('''select tbl_name, sql From sqlite_master''')
pp.pprint(cursor.fetchall())


cursor.execute('''ALTER TABLE vendors RENAME TO vendors_old''')
cursor.execute('''create table vendors (
    id_vendor INTEGER NOT NULL,
    name char(50) NOT NULL,
    city char(30) NOT NULL,
    address char(100) NOT NULL,
    constraint PK_vendors_id_vendor PRIMARY KEY (id_vendor),
    CONSTRAINT UQ_vendors_name_city Unique(name, city)
    )''')
cursor.execute('''INSERT INTO vendors (id_vendor, name, city, address)
SELECT id_vendor, name, city, address
FROM vendors_old;
''')
cursor.execute('''DROP TABLE vendors_old''')
connect.commit()

cursor.execute('''create table IF NOT EXISTS customers(
  id_customer INTEGER, 
  name char(50) NOT NULL,
  email char(50) NOT NULL,
  CONSTRAINT PK_customers_id_customer PRIMARY KEY (id_customer),
  CONSTRAINT UQ_customers_email UNIQUE (email)  
)''')

cursor.execute('''
create table IF NOT EXISTS vendors (
  id_vendor INTEGER,
  name char(50) NOT NULL,
  city char(30)NOT NULL,
  address char(100)NOT NULL,
  CONSTRAINT PK_vendors_id_vendor PRIMARY KEY(id_vendor)
)''')

cursor.execute('''
create table IF NOT EXISTS products (
  id_product INTEGER,
  name char(100) NOT NULL,
  author  char(50) NOT NULL,
  CONSTRAINT PK_products_id_product PRIMARY KEY (id_product) 
)''')

cursor.execute('''
create table IF NOT EXISTS prices (
  id_product int NOT NULL,
  date_price_changes date NOT NULL,
  price double NOT NULL,
  CONSTRAINT PK_prices PRIMARY KEY(id_product,date_price_changes),
  CONSTRAINT FK_prices_id_product FOREIGN KEY (id_product) REFERENCES products(id_product),
  CONSTRAINT CK_prices_price CHECK (price > 0) 
  )''')

cursor.execute('''
create table IF NOT EXISTS sale (
  id_sale INTEGER,
  id_customer int NOT NULL,
  date_sale timestamp NOT NULL DEFAULT NOW,
  CONSTRAINT PK_sale_id_sale PRIMARY KEY(id_sale),
  CONSTRAINT FK_sale_id_customer FOREIGN KEY (id_customer)  REFERENCES customers (id_customer)
)''')

cursor.execute('''
create table IF NOT EXISTS incoming (
  id_incoming INTEGER,
  id_vendor int NOT NULL,
  date_incoming timestamp NOT NULL DEFAULT NOW,
  CONSTRAINT PK_incoming_id_incoming PRIMARY KEY (id_incoming),
  CONSTRAINT FK_incoming_id_vendor FOREIGN KEY (id_vendor)  REFERENCES vendors (id_vendor)
)''')

cursor.execute('''
create table IF NOT EXISTS magazine_sales (
  id_sale int NOT NULL,
  id_product int NOT NULL,
  quantity int NOT NULL,
  CONSTRAINT PK_prices PRIMARY KEY(id_sale, id_product),
  CONSTRAINT FK_magazine_sales_id_sale FOREIGN KEY (id_sale)  REFERENCES sale (id_sale),
  CONSTRAINT FK_magazine_sales_id_product FOREIGN KEY (id_product)  REFERENCES products (id_product),
  CONSTRAINT CK_magazine_sales_quantity CHECK (quantity > 0)
  )''')

cursor.execute('''
create table IF NOT EXISTS magazine_incoming (
  id_incoming int NOT NULL,
  id_product int NOT NULL,
  quantity int NOT NULL,
  CONSTRAINT PK_magazine_incoming PRIMARY KEY (id_incoming, id_product),
  CONSTRAINT FK_magazine_incoming_id_incoming FOREIGN KEY (id_incoming) REFERENCES incoming (id_incoming),
  CONSTRAINT FK_magazine_incoming_id_product FOREIGN KEY (id_product) REFERENCES products (id_product),
  CONSTRAINT CK_magazine_sales_quantity CHECK (quantity > 0)
)''')

# Заполнение базы
customers = [
    ('Иванов Сергей', 'sergo@mail.ru'),
    ('Ленская Катя', 'lenskay@yandex.ru'),
    ('Демидов Олег', 'demidov@gmail.ru'),
    ('Афанасьев Виктор', 'victor@mail.ru'),
    ('Пажская Вера', 'verap@rambler.ru')
]

vendors = [('Вильямс', 'Москва', 'ул.Лесная, д.43'),
           ('Дом печати', 'Минск', 'пр.Ф.Скорины, д.18'),
           ('БХВ-Петербург', 'Санкт-Петербург', 'ул.Есенина, д.5')
        ]

products = [('Стихи о любви', 'Андрей Вознесенский'),
            ('Собрание сочинений, том 2', 'Андрей Вознесенский'),
            ('Собрание сочинений, том 3', 'Андрей Вознесенский'),
            ('Русская поэзия', 'Николай Заболоцкий'),
            ('Машенька', 'Владимир Набоков'),
            ('Доктор Живаго', 'Борис Пастернак'),
            ('Наши', 'Сергей Довлатов'),
            ('Приглашение на казнь', 'Владимир Набоков'),
            ('Лолита', 'Владимир Набоков'),
            ('Темные аллеи', 'Иван Бунин'),
            ('Дар', 'Владимир Набоков'),
            ('Сын вождя', 'Юлия Вознесенская'),
            ('Эмигранты', 'Алексей Толстой'),
            ('Горе от ума', 'Александр Грибоедов'),
            ('Анна Каренина', 'Лев Толстой'),
            ('Повести и рассказы', 'Николай Лесков'),
            ('Антоновские яблоки', 'Иван Бунин'),
            ('Мертвые души', 'Николай Гоголь'),
            ('Три сестры', 'Антон Чехов'),
            ('Беглянка', 'Владимир Даль'),
            ('Идиот', 'Федор Достоевский'),
            ('Братья Карамазовы', 'Федор Достоевский'),
            ('Ревизор', 'Николай Гоголь'),
            ('Гранатовый браслет', 'Александр Куприн')
        ]

prices = [(1, '2011-04-10', 100),
          (2, '2011-04-10', 130),
          (3, '2011-04-10', 90),
          (4, '2011-04-10', 100),
          (5, '2011-04-10', 110),
          (6, '2011-04-10', 85),
          (7, '2011-04-11', 95),
          (8, '2011-04-11', 100),
          (9, '2011-04-11', 79),
          (10, '2011-04-11', 49),
          (11, '2011-04-11', 105),
          (12, '2011-04-12', 85),
          (13, '2011-04-12', 135),
          (14, '2011-04-12', 100),
          (15, '2011-04-12', 90),
          (16, '2011-04-12', 75),
          (17, '2011-04-12', 90),
          (18, '2011-04-10', 150),
          (19, '2011-04-10', 140),
          (20, '2011-04-10', 85),
          (21, '2011-04-11', 105),
          (22, '2011-04-11', 70),
          (23, '2011-04-11', 65),
          (24, '2011-04-11', 130)
        ]

incoming = [(3, '2011-04-10'),
            (1, '2011-04-11'),
            (2, '2011-04-12')
        ]

magazine_incoming = [(1, 1, 10),
                     (1, 2, 5),
                     (1, 3, 7),
                     (1, 4, 10),
                     (1, 5, 10),
                     (1, 6, 8),
                     (1, 18, 8),
                     (1, 19, 8),
                     (1, 20, 8),
                     (2, 7, 10),
                     (2, 8, 10),
                     (2, 9, 6),
                     (2, 10, 10),
                     (2, 11, 10),
                     (2, 21, 10),
                     (2, 22, 10),
                     (2, 23, 10),
                     (2, 24, 10),
                     (3, 12, 10),
                     (3, 13, 10),
                     (3, 14, 10),
                     (3, 15, 10),
                     (3, 16, 10),
                     (3, 17, 10)
    ]

sale = [(2, '2011-04-11'),
        (3, '2011-04-11'),
        (5, '2011-04-11')
    ]

magazine_sales = [(1, 1, 1),
                  (1, 5, 1),
                  (1, 7, 1),
                  (2, 2, 1),
                  (3, 1, 1),
                  (3, 7, 1)
    ]

cursor.executemany("INSERT INTO customers(name,email) VALUES(?,?)", customers)
cursor.executemany("INSERT INTO vendors(name,city,address) VALUES(?,?,?)", vendors)
cursor.executemany("INSERT INTO products(name,author) VALUES(?,?)", products)
cursor.executemany("INSERT INTO prices VALUES(?,?,?)", prices)
cursor.executemany("INSERT INTO sale(id_customer, date_sale) VALUES(?,?)", sale)
cursor.executemany("INSERT INTO incoming(id_vendor, date_incoming) VALUES(?,?)", incoming)
cursor.executemany("INSERT INTO magazine_sales VALUES(?,?,?)", magazine_sales)
cursor.executemany("INSERT INTO magazine_incoming VALUES(?,?,?)", magazine_incoming)
connect.commit()

connect.close()
connect.close()
