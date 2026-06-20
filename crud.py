from fastapi import FastAPI,status
from pydantic import BaseModel
from fastapi.exceptions import HTTPException

books=[
    {
        "id":1,
        "title":"Book 1",
        "author":"Author 1",
        "year":2020
    },
    {
        "id":2,
        "title":"Book 2",
        "author":"Author 2",
        "year":2021
    },{
        "id":3,
        "title":"Book 3",
        "author":"Author 3",
        "year":2022
    },{
        "id":4,
        "title":"Book 4",
        "author":"Author 4",
        "year":2023
    },{
        "id":5,
        "title":"Book 5",
        "author":"Author 5",
        "year":2024
    }
]
app=FastAPI()

@app.get("/books")
def get_books():
    return books

@app.get("/books/{books_id}")
def get_book(books_id:int):
    for i in books:
        if i['id']==books_id: #looping throught list of dictonary
            return i            # 'id' --is the dictonary of the i th list

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="book not found")


#put and post method requires pydantic class
class Book(BaseModel):#pydantic class
    id:int
    title:str
    author:str
    year:int

@app.post("/books")
def create_book(book:Book):#the Book is from the above pydantic class
    new_book=book.model_dump() #to serialize a model in dictonary
    books.append(new_book)
    return books

class Bookupdate(BaseModel):
    title:str
    author:str
    year:int
@app.put("/books/{book_id}") #as because we have to fetch and update that particular book
def update_book(book_id:int,book_update:Bookupdate):
    for i in books:
        if(i['id']==book_id):
            i['title']=book_update.title
            i['author']=book_update.author
            i['year']=book_update.year
            return books

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.delete("/books/{book_id}")
def delete_book(book_id:int):
    for i in books:
        if(i['id']==book_id):
            books.remove(i)
            return {"Message":f"Book no-{book_id} deleted"},books
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")