import datetime
import random
import itertools

from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import create_engine, MetaData, Table, select, func, text, Column, String, Integer, Date, ForeignKey
from sqlalchemy.ext.automap import automap_base

Base = declarative_base()
metadata = MetaData()

class Books(Base):
    __tablename__ = 'books'

    book_id = Column(Integer, primary_key = True)
    title = Column(String(100), nullable = False)
    author = Column(String(100), nullable = False)
    published = Column(Integer, nullable = False)
    date_added = Column(Date, nullable = False)
    date_deleted = Column(Date, nullable = True)

class Borrows(Base):
    __tablename__ = 'borrows'

    borrow_id = Column(Integer, primary_key = True)
    book_id = Column(Integer, ForeignKey("books.book_id"))
    date_start = Column(Date, nullable=False)
    date_end = Column(Date, nullable=True)
    user_id = Column(Integer, nullable=False)

    book = relationship('Books')

