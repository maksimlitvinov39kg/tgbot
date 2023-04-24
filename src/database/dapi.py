from .models import Books, Borrows
import datetime
import random
import itertools
import pandas
import json
#$ pip install xlwt
#$ pip install openpyxl



from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import create_engine, MetaData, Table, select, func, text, Column, String, Integer, Date, delete
from sqlalchemy.ext.automap import automap_base

USERNAME = "domingol"
DATABASE_NAME = 'EPICDATABASE'
connection_string = f"postgresql+psycopg2://{USERNAME}:@localhost:5431/{DATABASE_NAME}"
engine = create_engine(connection_string)
Session = sessionmaker(engine)
meta = MetaData()
meta.reflect(engine)


class DatabaseConnector():

    def borrows_to_file(bookid: int) -> str:
        filename = f'book_{bookid}_borrows.xlsx'
        with Session() as session:
            query = select(Borrows).where(Borrows.book_id == bookid).with_only_columns(
                Borrows.borrow_id, Borrows.book_id, Borrows.date_start, Borrows.date_end)
            pandas.read_sql(query, session.connection()).to_excel(filename)
        return filename

    def add(self,title, author, published):
        with Session() as session:
            newbook = Books(title = title,author = author,published = published,date_added = datetime.datetime.now())
            try:
                session.add(newbook)
                session.commit()
                return newbook.book_id
            except Exception as e:
                print(e)
                return False

    def delete(self, book_id):
        with Session() as session:
            try:
                borrow = session.query(Borrows).filter_by(book_id=book_id).first()
                if borrow is not None:
                    return False
                book = session.query(Books).filter_by(book_id=book_id).first()
                if book is not None:
                    session.delete(book)
                    session.commit()
                    session.close()
                    return True
                else:
                    return False
            except Exception as e:
                session.close()
                print(e)
                return False

    def list_books(self):
        list = []
        with Session() as session:
            try:
                books = session.query(Books).all()
                session.close()
                for book in books:
                    book_dict = {
                        'book_id': book.book_id,
                        'title': book.title,
                        'author': book.author,
                        'published': book.published,
                        'date_added': book.date_added
                    }
                    list.append(book_dict)
                return list
            except Exception as e:
                session.close()
                print(e)
                return []

    def get_book(self, title, author, published):
        with Session() as session:
            try:
                book_id = session.query(Books).filter_by(title=title, author=author, published = published).first()
                if (book_id is not None):
                    session.close()
                    return book_id
                else:
                    session.close()
                    return None
            except Exception:
                session.close()
                print(Exception)
                return None

    def get_book_by_id(self, id):
        with Session() as session:
            try:
                book_id = session.query(Books).filter_by(book_id = id).first()
                if (book_id is not None):
                    session.close()
                    return book_id
                else:
                    session.close()
                    return None
            except Exception:
                session.close()
                print(Exception)
                return None

    def borrow(self, book_id, user_id):
        with Session() as session:
            try:
                borrow = session.query(Borrows).filter_by(book_id=book_id, date_end=None).first()
                if (borrow is not None):
                    session.close()
                    return False
                borrow = Borrows(book_id=book_id, user_id=user_id, date_start=datetime.date.today())
                session.add(borrow)
                session.commit()
                borrow_id = borrow.borrow_id
                session.close()
                return borrow_id
            except Exception as e:
                session.close()
                print(e)
                return False

    def get_borrow(self, user_id):
        with Session() as session:
            try:
                borrow = session.query(Borrows).filter(Borrows.user_id == user_id).first()
                if borrow:
                    return borrow
                else:
                    return False
            except Exception as e:
                print(e)
                return False
            finally:
                session.close()

    def retrieve(self, borrow_id, date_end):
        with Session() as session:
            try:
                borrow = session.query(Borrows).filter(Borrows.borrow_id == borrow_id).first()
                if borrow:
                    borrow.date_end = date_end
                    session.commit()
                    session.close()
                    return True
                else:
                    return False
            except Exception:
                print(Exception)
                session.rollback()
                return False

