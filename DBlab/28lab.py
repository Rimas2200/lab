import sqlite3
import pprint

connect = sqlite3.connect('db_books.sqlite')
cursor = connect.cursor()
pp = pprint.PrettyPrinter(indent=10, width=80, compact=False)

cursor.execute('''drop trigger if exists after_delete_items ''')
cursor.execute('''drop trigger if exists after_insert_items''')
cursor.execute('''drop trigger if exists after_update_items''')
cursor.execute('''drop trigger if exists after_insert_items_b_rest''')
cursor.execute('''drop trigger if exists after_update_items_b_rest''')
cursor.execute('''drop trigger if exists after_delete_items_b_rest''')

# Задание 1
cursor.execute('''
    create table if not exists A (
        A_ID_old int,
        A_ID_new int,
        A_contr_old numeric(6),
        A_contr_new int(6),
        A_count_old int(4),
        A_count_new int(4),
        A_date text,
        operation varchar(7),
        constraint CK_A_operation check (operation in('delete','insert','update'))
)''')

# Задание 2
# delete
cursor.execute('''
    create trigger if not exists after_delete_items
    after delete on items
    for each row
    begin
      insert into A values (old.i_id, null, old.i_contract, null, old.i_count, null, datetime('now'), 'delete');
    end
''')
# update
cursor.execute('''
    create trigger if not exists after_update_items
    after update on items
    for each row
    begin
      insert into A values (old.i_id, new.i_id, old.i_contract, new.i_contract, old.i_count, new.i_count, datetime('now'), 'update');
    end
''')
# insert
cursor.execute('''
    create trigger if not exists after_insert_items
    after insert on items
    for each row
    begin
      insert into A values (null, new.i_id, null, new.i_contract, null, new.i_count, datetime('now'), 'insert');
    end
''')

# Задание 3
cursor.execute('''delete from A''')
cursor.execute('''delete from items''')
connect.commit()

cursor.execute('''insert into items values (1, 100001, 150),
                                      (2, 100012, 100),
                                      (3, 100021, 200)''')
cursor.execute('''update items set i_count = 2*i_count''')
cursor.execute('''delete from items''')
connect.commit()

cursor.execute('''select * from A''')
pp.pprint(cursor.fetchall())

# Задание 4
# insert
cursor.execute('''
    create trigger if not exists after_insert_items_b_rest
    after insert on items
    for each row
    when (select b_rest from books where b_contract = new.i_contract) >= new.i_count
    begin
      insert into A values(null, new.i_id, null, new.i_contract, null, new.i_count, datetime('now'), 'insert');
      update books set b_rest = b_rest - new.i_count
      where b_contract = new.i_contract;
    end
''')
# update
cursor.execute('''
    create trigger if not exists after_update_items_b_rest
    after update on items
    for each row
    when (select b_rest from books where b_contract = new.i_contract) >= (new.i_count - old.i_count)
    begin
      insert into A values(old.i_id, new.i_id, old.i_contract, new.i_contract, old.i_count, new.i_count, datetime('now'), 'update');
      update books set b_rest = b_rest - (new.i_count - old.i_count)
      where b_contract = new.i_contract;
    end
''')
# delete
cursor.execute('''
    create trigger if not exists after_delete_items_b_rest
    after delete on items
    for each row
    begin
      insert into A values(old.i_id, null, old.i_contract, null, old.i_count, null, datetime('now'), 'delete');
      update books set b_rest = b_rest + old.i_count
      where b_contract = old.i_contract;
    end
''')

# 5.1
cursor.execute('''select * from books''')
pp.pprint(cursor.fetchall())
# 5.2
cursor.execute('''select * from Orders''')
pp.pprint(cursor.fetchall())
# 5.3
cursor.execute('''select * from items''')
pp.pprint(cursor.fetchall())
# 5.4
cursor.execute('''select * from books''')
pp.pprint(cursor.fetchall())
# 5.5
cursor.execute('''delete from items''')
connect.commit()
# 5.6
cursor.execute('''select * from books''')
pp.pprint(cursor.fetchall())
# 5.7
cursor.execute('''insert into items values (1, 100001, 150)''')
cursor.execute('''update items set i_count = 200 where i_id = 1''')
connect.commit()
# 5.8
cursor.execute('''select * from books''')
pp.pprint(cursor.fetchall())



# 1
print("\n1. Проверка остатка перед вставкой новой записи в items:")
contract_check = 100001
requested_count = 50

# Проверка достаточности остатка в таблице books
cursor.execute('''
SELECT b_rest 
FROM books 
WHERE b_contract = ?
''', (contract_check,))
book_stock = cursor.fetchone()

if book_stock and book_stock[0] >= requested_count:
    print(f"Остаток достаточен ({book_stock[0]}). Вставляем запись.")
    cursor.execute('''INSERT INTO items (i_id, i_contract, i_count) VALUES (NULL, ?, ?)''',
              (contract_check, requested_count))
    connect.commit()
else:
    print(f"Недостаточно остатка для заказа. Остаток: {book_stock[0] if book_stock else 'Не найден контракт'}")

# 2
print("\n2. Проверка содержимого таблицы items после вставки:")
cursor.execute('''SELECT * FROM items''')
pp.pprint(cursor.fetchall())

# 3
print("\n3. Обновление записи в items:")
update_id = 1
new_count = 300

# Проверка перед обновлением, что остатка хватает для нового значения
cursor.execute('''
SELECT b_rest 
FROM books 
WHERE b_contract = (SELECT i_contract FROM items WHERE i_id = ?)
''', (update_id,))
book_stock_update = cursor.fetchone()

if book_stock_update and book_stock_update[0] >= (new_count - 150):
    print(f"Остаток достаточен для обновления. Выполняем обновление записи.")
    cursor.execute('''UPDATE items SET i_count = ? WHERE i_id = ?''', (new_count, update_id))
    connect.commit()
else:
    print(
        f"Недостаточно остатка для обновления. Остаток: {book_stock_update[0] if book_stock_update else 'Не найден контракт'}")

# 4
print("\n4. Проверка содержимого таблицы items после обновления:")
cursor.execute('''SELECT * FROM items''')
pp.pprint(cursor.fetchall())

# 5
print("\n5. Удаление записи из items:")
delete_id = 1  # Пример ID для удаления

cursor.execute('''
SELECT i_contract, i_count 
FROM items 
WHERE i_id = ?
''', (delete_id,))
item_to_delete = cursor.fetchone()

if item_to_delete:
    contract_to_delete = item_to_delete[0]
    count_to_delete = item_to_delete[1]

    print(f"Удаляем запись с i_id = {delete_id} (контракт: {contract_to_delete}, количество: {count_to_delete}).")
    cursor.execute('''DELETE FROM items WHERE i_id = ?''', (delete_id,))
    connect.commit()
else:
    print("Запись с таким i_id не найдена для удаления.")

# 6
print("\n6. Проверка содержимого таблицы items после удаления:")
cursor.execute('''SELECT * FROM items''')
pp.pprint(cursor.fetchall())

# 7
print("\n7. Проверка остатков в таблице books после удаления из items:")
cursor.execute('''SELECT * FROM books''')
pp.pprint(cursor.fetchall())


# cursor.execute('''PRAGMA foreign_keys = 1''')
# cursor.execute('''drop table if exists editors''')
# cursor.execute('''drop table if exists titles''')
# cursor.execute('''drop table if exists items''')
# cursor.execute('''drop table if exists authors''')
# cursor.execute('''drop table if exists orders''')
# cursor.execute('''drop table if exists customers''')
# cursor.execute('''drop table if exists books''')
# cursor.execute('''drop table if exists employees''')
# cursor.execute('''drop table if exists posts''')
# cursor.execute('''drop table if exists rooms''')

cursor.execute('''create table if not exists posts (
    p_id  integer,
    p_post  varchar(30) not null,
    p_sal  numeric(8,2)  not null,
    constraint PK_posts_p_id primary key(p_id),
    constraint CK_posts_p_sal check(p_sal > 0)
    )
''')

cursor.execute('''
    create table if not exists rooms (
    r_no numeric(3) not null,
    r_tel varchar(10),
    constraint UQ_rooms unique(r_no, r_tel)
)''')

cursor.execute('''
    create table if not exists employees (
    e_tab numeric(4),
    e_fname varchar(20) not null,
    e_lname varchar(30) not null,
    e_born date,
    e_gender char(1) not null check(e_gender in ('м','ж')),
    e_post numeric(3),
    e_room numeric(3),
    e_tel varchar(10),
    e_inn char(12) not null,
    e_passp char(12) not null,
    e_org varchar(30) not null,
    e_pdate date not null,
    e_addr varchar(50),
    constraint PK_employees_e_tab primary key(e_tab),
    constraint FK_employees_e_fname foreign key(e_post) references posts (p_id),
    constraint FK_employees_room_tel foreign key(e_room,e_tel) references rooms(r_no,r_tel)
)''')

cursor.execute('''
    create table if not exists customers (
    c_id integer,
    c_name varchar(30) not null,
    c_addr varchar(30) not null,
    constraint PK_customers_c_id primary key(c_id)
)''')

cursor.execute('''
    create table if not exists authors (
    a_id integer,
    a_fname varchar(20) not null,
    a_lname varchar(30) not null,
    a_inn char(12),
    a_passp char(12) not null,
    a_org varchar(30) not null,
    a_pdate date not null,
    a_addr varchar(50) not null,
    a_tel varchar(30),
    constraint PK_authors primary key(a_id),
    constraint UQ_authors_a_inn unique(a_inn)
)''')

cursor.execute('''
    create table if not exists books (
    b_contract int(6),
    b_date date not null,
    b_man numeric(4) check (b_man in (1003, 1004)),
    b_title varchar(40) not null,
    b_price numeric(6, 2),
    b_advance numeric(10, 2),
    b_fee numeric(8, 2),
    b_publ date,
    b_circul int(5),
    b_edit numeric(4) check (b_edit in (1006)),
    b_rest int(5),
    constraint PK_books_contract primary key(b_contract),
    constraint FK_books_man foreign key(b_man) references employees(e_tab),
    constraint FK_books_man foreign key(b_edit) references employees(e_tab)
)''')

cursor.execute('''
    create table if not exists orders (
    o_id integer,
    o_company numeric(4),
    o_date date not null,
    o_ready date,
    constraint PK_orders_id primary key(o_id),
    constraint FK_orders_company foreign key(o_company) references customers(c_id)
)''')

cursor.execute('''
    create table if not exists titles (
    t_contract int(6),
    t_id int(4),
    t_number int(1) not null,
    t_percent int(3),
    constraint PK_titles primary key(t_contract, t_id),
    constraint CK_titles_percent check(t_percent >= 0 and t_percent <= 100),
    constraint FK_titles_contract foreign key(t_contract) references books(b_contract),
    constraint FK_titles_id foreign key(t_id) references authors(a_id)
)''')

cursor.execute('''
    create table if not exists items (
    i_id int(6),
    i_contract int(6),
    i_count int(4) not null,
    constraint PK_items primary key(i_id, i_contract),
    constraint FK_items_id foreign key(i_id) references orders(o_id),
    constraint FK_items_contract foreign key(i_contract) references books(b_contract)
)''')

cursor.execute('''
    create table if not exists editors (
    e_contract int(6),
    e_id int(4),
    constraint PK_editors primary key(e_contract, e_id),
    constraint FK_editors_contract foreign key(e_contract) references books(b_contract),
    constraint FK_editors_id foreign key(e_id) references employees(e_tab)
)''')

posts = [('editor',100.2), ('manager',200.2), ('director',300.2), ('main editor',150.2)]

cursor.executemany("INSERT INTO posts(p_post, p_sal) VALUES(?, ?)", posts)
connect.commit()

rooms = [(1,'555-551'), (2,'555-552'), (3,'555-553'), (4,'555-554'), (5,'555-555'), (6,'555-556')]

cursor.executemany("INSERT INTO rooms VALUES(?, ?)", rooms)
connect.commit()


employees = [
    (1001,'Мирон','Фролов','01.01.1980','м',1,1,'555-551','1234567890','7504 12341','abracadabra','01.01.1999','Makeeva 34'),
    (1002,'Игорь','Фролов','01.01.1981','м',1,2,'555-552','1234567891','7504 12342','abracadabra','01.01.1998','Makeeva 35'),
    (1003,'Иван','Иванов','01.01.1982','м',2,3,'555-553','1234567892','7504 12343','abracadabra','01.01.1997','Makeeva 36'),
    (1004,'Мирон','Соколов','01.01.1983','м',2,4,'555-554','1234567893','7504 12344','abracadabra','01.01.1996','Makeeva 37'),
    (1005,'Виктор','Дремин','01.01.1984','м',3,5,'555-555','1234567894','7504 12345','abracadabra','01.01.1995','Makeeva 38'),
    (1006,'Дмитрий','Сидоров','01.01.1985','м',4,6,'555-556','1234567895','7504 12346','abracadabra','01.01.1994','Makeeva 39')
]

cursor.executemany("INSERT INTO employees VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", employees)
connect.commit()

books = [(100001,'2021-01-12',1004,'Стихи о любви',450,2000000,100000, '2021-04-01',1000,1006,1000),
    (100002, '2021-01-12',1003,'Собрание сочинений, том 2',950, 2000000,100000, '2021-04-01',1000,1006,1000),
    (100003, '2021-01-12',1004,'Собрание сочинений, том 3',300, 2000000,100000, '2021-04-01',1000,1006,1000),
    (100004, '2021-01-12',1004,'Русская поэзия',1450, 2000000,100000, '2021-04-01',3000,1006,3000),
    (100005, '2021-01-12',1003,'Машенька',1350, 2000000,100000, '2021-04-01',1000,1006,1000),
    (100006, '2021-01-12',1004,'Доктор Живаго',450, 2000000,100000, '2021-04-01',1000,1006,1000),
    (100007, '2021-01-12',1003,'Наши',450, 2000000,100000, '2021-04-01',1000,1006,1000),
    (100008, '2021-01-12',1004,'Приглашение на казнь',450, 2000000,100000, '2021-04-01',1000,1006,1000),
    (100009, '2021-01-12',1004,'Лолита',950, 2000000,100000, '2021-04-01' ,1000,1006,1000),
    (100010, '2021-01-12',1003,'Темные аллеи',450, 2000000,100000, '2021-04-01',1000,1006,1000),
    (100011, '2021-01-12',1004,'Дар',450, 2000000,100000,  '2021-04-01',1000,1006,1000),
    (100012, '2021-01-12',1004,'Сын вождя',450, 2000000,100000, '2021-04-01',1000,1006,1000),
    (100013, '2021-01-12',1003,'Эмигранты',1450, 2000000,100000, '2021-04-01',1000,1006,1000),
    (100014, '2021-04-01',1003,'Горе от ума',1450, 2000000,100000, '2021-01-12',1000,1006,1000)
]
cursor.executemany("INSERT INTO books VALUES(?,?,?,?,?,?,?,?,?,?,?)", books)
connect.commit()

cursor.execute('''insert into customers(c_name, c_addr) values ('Заказчик1', 'Адрес1'),
    ('Заказчик2', 'Адрес2'),
    ('Заказчик3', 'Адрес3'),
    ('Заказчик4', 'Адрес4')
''')

cursor.execute('''insert into authors(a_fname, a_lname, a_inn, a_passp, a_org, a_pdate, a_addr, a_tel)
    values('Фамилия1', 'Имя1', '741234123411', '1234 N123456', 'Организация1', '2000-01-01', 'адрес1','+798111111'),
    ('Фамилия2', 'Имя2', '741234123412', '1234 N123456', 'Организация2', '2000-01-01', 'адрес1','+798111111'),
    ('Фамилия3', 'Имя3', '741234123413', '1234 N123456', 'Организация3', '2000-01-01', 'адрес1','+798111111'),
    ('Набоков', 'Владимир', '741234123414', '1234 N123456', 'Организация4', '2000-01-01', 'адрес1','+798111111'),
    ('Грибоедов', 'Александр', '741234123415', '1234 N123456', 'Организация5', '2000-01-01', 'адрес1','+798111111'),
    ('Пастернак', 'Борис', '741234123416', '1234 N123456', 'Организация6', '2000-01-01', 'адрес1','+798111111'),
    ('Цветаева', 'Марина', '741234123417', '1234 N123456', 'Организация7', '2000-01-01', 'адрес1','+798111111')

''')

cursor.execute('''insert into orders(o_company, o_date, o_ready)
    values(4, '2001-02-03', '2001-05-03'),
    (2, '2001-01-03', '2001-04-03'),
    (1, '2001-05-03', '2001-06-03'),
    (2, '2001-08-03', '2001-09-03')'''
)

cursor.execute('''insert into items
    values(1, 100005, 50),
    (1, 100009, 60),
    (1, 100014, 60),
    (2, 100005, 40),
    (2, 100001, 100),
    (2, 100002, 10),
    (3, 100002, 10),
    (3, 100006, 10),
    (4, 100011, 80)'''
)

connect.commit()

editors = [(100001,1001),
    (100002,1001),
    (100003,1001),
    (100004,1001),
    (100005,1001),
    (100006,1001),
    (100007,1001),
    (100008,1001),
    (100009,1001),
    (100010,1001),
    (100011,1001),
    (100012,1001),
    (100013,1001),
    (100014,1001),
    (100001,1002),
    (100002,1002),
    (100003,1002),
    (100004,1002),
    (100005,1002),
    (100006,1002),
    (100007,1002),
    (100008,1002),
    (100009,1002),
    (100010,1002)
]

cursor.executemany("INSERT INTO editors VALUES(?,?)", editors)
connect.commit()


cursor.cursor.execute('''insert into titles
    values(100005, 2, 1, 100),
    (100009, 2, 1, 100),
    (100011, 3, 1, 100),
    (100014, 2, 1, 100),
    (100006, 3, 1, 100),
    (100001, 1, 1, 100),
    (100002, 1, 1, 100)'''
)
connect.commit()
connect.close()

