
import  sqlalchemy as sq
from  sqlalchemy.orm import  declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    def __str__(self):
        return  f' Publisher {self.id}:{self.name}'

class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    def __str__(self):
        return  f' Shop {self.id}:{self.name}'

class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    publisher = relationship(Publisher, backref='books')

    def __str__(self):
        return  f' Book {self.id},({self.title}, {self.id_publisher})\n'

class Stock(Base) :
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer,primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    book = relationship(Book, backref='stocks')
    shop = relationship(Shop, backref='stocks')
    def __str__(self):
        return  f' Stock {self.id},(книга №{self.id_book}, проданы в магазине {self.id_shop}, в количестве {self.count} штук)\n'

class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Integer, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship(Stock, backref='sales')

    def __str__(self):
        return f' Sales {self.id}, по цене {self.price} рублей, дата {self.date_sale}, сток № {self.id_stock}\n'


def create_tables(engine):

    Base.metadata.create_all(engine)

