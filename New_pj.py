import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


class pPublisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=80), unique=True)

    def __str__(self):
        return f'{self.id}: {self.name}'

class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=80), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(pPublisher, backref="publishers")

class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=80), unique=True)

class Stock(Base):
    __tablename__ = "stock"
    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer)

    shop = relationship(Shop, backref="shop")
    book = relationship(Book, backref="books")

class Sale(Base):
    __tablename__ = "sale"
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.BIGINT)
    date_sale = sq.Column(sq.VARCHAR(80))
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer)
    stock = relationship(Stock, backref="stock")

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

DSN = "postgresql://postgres:Alex2905@localhost:5432/my_db"
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

Publisher = pPublisher(name="Erich Maria Remarque")

session.add(Publisher)
session.commit()

print(Publisher.id, Publisher.name)
def get():
    name = input("Enter the publisher's name: ")
    #name = "Erich Maria Remarque"
    publisher = session.query(pPublisher).filter(pPublisher.name.like(name)).one()
    print(publisher)
get()
session.close()

