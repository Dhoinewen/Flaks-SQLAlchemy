import sqlalchemy as db
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


conn = create_engine("postgresql+psycopg2://postgres:123456@localhost/test4")
metadata = MetaData()

Session = sessionmaker()
session = Session(bind=conn)

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(30), nullable=False)
    want_to_read = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'{self.id}'

#Base.metadata.create_all(bind=conn)

book = Book(title='The Hobbit',
            author='John R. R. Tolkien', want_to_read=False)
session.add(book)
session.commit()

rows = session.query(Book).filter(Book.author == 'John R. R. Tolkien').all()
print('Query by SqlAlchemy ORM:', rows)


