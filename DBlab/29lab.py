import sqlite3
import pprint

connect = sqlite3.connect('db_books.sqlite')
cursor = connect.cursor()
pp = pprint.PrettyPrinter(indent=2, width=80)

script = '''
    PRAGMA foreign_keys = ON;
    
    -- Удаляем старые триггеры
    DROP TRIGGER IF EXISTS before_insert_items_b_rest;
    DROP TRIGGER IF EXISTS after_insert_items_b_rest;
    DROP TRIGGER IF EXISTS before_update_items_b_rest;
    DROP TRIGGER IF EXISTS after_update_items_b_rest;
    DROP TRIGGER IF EXISTS after_delete_items_b_rest;
    DROP TRIGGER IF EXISTS after_insert_items;
    DROP TRIGGER IF EXISTS after_update_items;
    DROP TRIGGER IF EXISTS after_delete_items;
    DROP TRIGGER IF EXISTS instead_of_insert_v;
    DROP TRIGGER IF EXISTS instead_of_update_v;
    DROP TRIGGER IF EXISTS instead_of_delete_v;
    
    -- Таблица-протокол изменений
    CREATE TABLE IF NOT EXISTS A (
        A_ID_old    INT,
        A_ID_new    INT,
        A_contr_old NUMERIC(6),
        A_contr_new NUMERIC(6),
        A_count_old INT,
        A_count_new INT,
        A_date      TEXT,
        operation   VARCHAR(7) CHECK(operation IN ('delete','insert','update'))
    );
    
    -- BEFORE INSERT: проверка остатка и RAISE
    CREATE TRIGGER before_insert_items_b_rest
    BEFORE INSERT ON items
    FOR EACH ROW
    WHEN (SELECT b_rest FROM books WHERE b_contract = NEW.i_contract) < NEW.i_count
    BEGIN
        SELECT RAISE(ABORT, 'Недостаточно остатка для контракта');
    END;
    
    -- AFTER INSERT: протоколируем и уменьшаем b_rest (не более 5 записей в A)
    CREATE TRIGGER after_insert_items_b_rest
    AFTER INSERT ON items
    FOR EACH ROW
    WHEN (SELECT COUNT(*) FROM A) < 5
    BEGIN
        INSERT INTO A VALUES(NULL, NEW.i_id, NULL, NEW.i_contract, NULL, NEW.i_count, datetime('now'), 'insert');
        UPDATE books
          SET b_rest = b_rest - NEW.i_count
          WHERE b_contract = NEW.i_contract;
    END;
    
    -- BEFORE UPDATE: проверка прироста и RAISE
    CREATE TRIGGER before_update_items_b_rest
    BEFORE UPDATE OF i_count ON items
    FOR EACH ROW
    WHEN (SELECT b_rest FROM books WHERE b_contract = NEW.i_contract) < (NEW.i_count - OLD.i_count)
    BEGIN
        SELECT RAISE(ABORT, 'Недостаточно остатка для обновления');
    END;
    
    -- AFTER UPDATE: протоколируем и уменьшаем b_rest
    CREATE TRIGGER after_update_items_b_rest
    AFTER UPDATE OF i_count ON items
    FOR EACH ROW
    WHEN (SELECT COUNT(*) FROM A) < 5
    BEGIN
        INSERT INTO A VALUES(OLD.i_id, NEW.i_id, OLD.i_contract, NEW.i_contract, OLD.i_count, NEW.i_count, datetime('now'), 'update');
        UPDATE books
          SET b_rest = b_rest - (NEW.i_count - OLD.i_count)
          WHERE b_contract = NEW.i_contract;
    END;
    
    -- AFTER DELETE: протоколируем и восстанавливаем b_rest
    CREATE TRIGGER after_delete_items_b_rest
    AFTER DELETE ON items
    FOR EACH ROW
    WHEN (SELECT COUNT(*) FROM A) < 5
    BEGIN
        INSERT INTO A VALUES(OLD.i_id, NULL, OLD.i_contract, NULL, OLD.i_count, NULL, datetime('now'), 'delete');
        UPDATE books
          SET b_rest = b_rest + OLD.i_count
          WHERE b_contract = OLD.i_contract;
    END;
    
    -- Представление для INSTEAD OF-триггеров
    CREATE VIEW IF NOT EXISTS v_order_items AS
    SELECT o.o_id AS order_id, o.o_date, i.i_contract, i.i_count
    FROM orders o JOIN items i ON o.o_id = i.i_id;
    
    -- INSTEAD OF INSERT на VIEW
    CREATE TRIGGER instead_of_insert_v
    INSTEAD OF INSERT ON v_order_items
    FOR EACH ROW
    BEGIN
        INSERT INTO items(i_id, i_contract, i_count)
        VALUES(NEW.order_id, NEW.i_contract, NEW.i_count);
    END;
    
    -- INSTEAD OF UPDATE на VIEW
    CREATE TRIGGER instead_of_update_v
    INSTEAD OF UPDATE ON v_order_items
    FOR EACH ROW
    BEGIN
        UPDATE items
          SET i_contract = NEW.i_contract,
              i_count    = NEW.i_count
        WHERE i_id = OLD.order_id;
    END;
    
    -- INSTEAD OF DELETE на VIEW
    CREATE TRIGGER instead_of_delete_v
    INSTEAD OF DELETE ON v_order_items
    FOR EACH ROW
    BEGIN
        DELETE FROM items WHERE i_id = OLD.order_id;
    END;
'''

connect.executescript(script)
connect.commit()

#Проверка
print("Список всех триггеров")
cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='trigger';")
pp.pprint(cursor.fetchall())

print("\nТриггеры для таблицы items")
cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='trigger' AND tbl_name='items';")
pp.pprint(cursor.fetchall())

# Тест
print("\nТест BEFORE INSERT RAISE ")
try:
    cursor.execute("INSERT INTO items(i_id, i_contract, i_count) VALUES (?,?,?);", (999, 100001, 100000000))
    connect.commit()
except sqlite3.DatabaseError as e:
    print("Ошибка вставки:", e)

print("\nСодержимое items после вставки")
cursor.execute("SELECT * FROM items;")
pp.pprint(cursor.fetchall())
print("\nОстатки в books после вставки")
cursor.execute("SELECT b_contract, b_rest FROM books WHERE b_contract=100001;")
pp.pprint(cursor.fetchall())

# Тест обновления
print("\nТест BEFORE UPDATE RAISE")
update_id = 2
try:
    cursor.execute("UPDATE items SET i_count = ? WHERE i_id = ?;", (100000000, update_id))
    connect.commit()
except sqlite3.DatabaseError as e:
    print("Ошибка обновления:", e)

print("\nСодержимое items после обновления")
cursor.execute("SELECT * FROM items;")
pp.pprint(cursor.fetchall())
print("\nОстатки в books после обновления")
cursor.execute("SELECT b_contract, b_rest FROM books WHERE b_contract=(SELECT i_contract FROM items WHERE i_id=?);", (update_id,))
pp.pprint(cursor.fetchall())

# Протокол изменений A
print("\nПротокол изменений A (последние 5)")
cursor.execute("SELECT * FROM A ORDER BY A_date DESC;")
pp.pprint(cursor.fetchall())

# Демонстрация CASE WHEN
print("\nСтатус остатков книг (CASE WHEN)")
cursor.execute('''
    SELECT b_contract,
      CASE
        WHEN b_rest < 0 THEN 'Нет в наличии'
        WHEN b_rest < 100 THEN 'Мало'
        ELSE 'В наличии'
      END AS stock_status
    FROM books;
''')
pp.pprint(cursor.cursor.fetchall())

connect.close()
