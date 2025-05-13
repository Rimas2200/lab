import sqlite3
import pprint

pp = pprint.PrettyPrinter(indent=1, width=40, compact=False)
connect = sqlite3.connect('db_shop.sqlite')
cursor = connect.cursor()

# cursor.execute('''drop view if exists prices_last''')
# cursor.execute('''drop view if exists vendors_incoming_magazine_prices''')
# cursor.execute('''drop view if exists vendors_incoming_magazine''')
# cursor.execute('''drop view if exists vendors_incoming''')

cursor.execute('''
    Create view if not exists prices_last as
    select distinct id_product, max(date_price_changes) over (partition by id_product) as date_price_changes,first_value(price) over (partition by id_product order by date_price_changes desc) as price
    From prices
''')

cursor.execute('''
    Create view if not exists vendors_incoming as
    select id_incoming,date_incoming, v.id_vendor, name, city, address
    From vendors v join incoming I on v.id_vendor=i.id_vendor
''')

cursor.execute('''
    Create view if not exists vendors_incoming_magazine as
    select i.id_incoming,date_incoming, v.id_vendor, name, city, address, id_product, quantity
    From vendors v join incoming I on v.id_vendor=i.id_vendor join magazine_incoming mi on i.id_incoming=mi.id_incoming
''')

cursor.execute('''
    Create view if not exists vendors_incoming_magazine_prices  as
    select * From vendors_incoming_magazine as vim join prices_last as p on vim.id_product=p.id_product 
''')

cursor.execute('Select *  From prices_last')

print ('Вывод из представления prices_last')
pp.pprint(cursor.fetchall())

cursor.execute('Select name,date_incoming From vendors_incoming')
print ('Вывод из представления vendors_incoming')
pp.pprint(cursor.fetchall())

cursor.execute('Select name,id_product, quantity   From vendors_incoming_magazine')
print ('Вывод из представления vendors_incoming_magazine')
pp.pprint(cursor.fetchall())

cursor.execute('Select id_incoming, name,id_product, quantity, price   From vendors_incoming_magazine_prices')
print ('Вывод из представления vendors_incoming_magazine_prices')
pp.pprint(cursor.fetchall())

cursor.execute('Select name, sum(quantity), sum(quantity*price) From vendors_incoming_magazine_prices group by id_incoming, name')
print ('Вывод из представления vendors_incoming_magazine')
pp.pprint(cursor.fetchall())

cursor.execute('''
    Select (select name from products where id_product=vimp.id_product) name_product, sum(quantity) as N, 
    sum(quantity*price) as S, max(sum(quantity*price)) over() as m   
    From vendors_incoming_magazine_prices as vimp group by id_product
''')

print ('Вывод из представления vendors_incoming_magazine_prices и таблицы Products ')
pp.pprint(cursor.fetchall())

cursor.execute('''
    Select name_product, s
    from (Select (select name from products where id_product=vimp.id_product) name_product, sum(quantity*price) as S, 
    max(sum(quantity*price)) over() as m  From vendors_incoming_magazine_prices as vimp group by id_product) as t
    where s=m
''')

print ('Предыдущий запрос использован как подзапрос для нахождения продукта с максиальной стоимостью ')
pp.pprint(cursor.fetchall())

connect.commit()
connect.close()
