#inserting data into the table

from fastapi import FastAPI , Depends
from database import get_db,engine
from sqlalchemy.orm import Session
import model
from pydantic import BaseModel

#creating api

app=FastAPI()

class Bookstore(BaseModel):
    id:int
    title:str
    author:str
    year:int

@app.post("/books")
def create_book(i:Bookstore,db:Session=Depends(get_db)):
    new_book=model.Book(id=i.id,title=i.title,author=i.author,year=i.year)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    db.close()
    return new_book

@app.get("/books")
def get_books(db:Session=Depends(get_db)):
    books=db.query(model.Book).all()
    db.close()
    return books