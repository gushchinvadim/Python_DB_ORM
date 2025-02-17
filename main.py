import psycopg2
import json
import sqlalchemy
import configparser
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale, find_data

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
# session.commit()


with psycopg2.connect(database=db, user=user, password=password) as conn:
    find_data(conn, f'{input("введите имя:")}')
conn.close()
session.close()

