import psycopg2
import json
import sqlalchemy
import configparser
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale

config = configparser.ConfigParser()
config.read('settings.ini')
DSN = config['DSN']['dsn']
db = config['DSN']['db']
user = config['DSN']['user']
password = config['DSN']['pass']
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()
session.commit()

with open('fixtures/test_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
# session.commit() #закоммитить после установки БД
def get_data(a):
    q = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).select_from(Publisher).join(Book).join(Stock).join(Shop).join(Sale)
    if  a.isdigit():
        x = q.filter(Publisher.id == a).all()
    else:
        x = q.filter(Publisher.name == a).all()

    for  book_title,shop_name,sale_price,sale_date_sale in x:
        print(f"{book_title:<20}|{shop_name:<10}|{sale_price:<5}|{sale_date_sale}")


session.close()

if __name__ == '__main__':

    get_data(a=input("Введите имя или ID: "))

