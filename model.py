from database import Base
from sqlalchemy import Column,Integer,VARCHAR
class Book(Base): #all the feature of the base class will be inherited to Book
    #it will become db table
    __tablename__="books" #tablename

    id = Column(Integer,primary_key=True,index=True)
    title=Column(VARCHAR(30))
    author=Column(VARCHAR(30))
    year=Column(Integer)