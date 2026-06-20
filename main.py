from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel


app=FastAPI() #creating app..INSTANCE of FAST API OBJECT

@app.get("/") #home directory
def read_root():
    return {"Message": "Hello world"}

@app.get("/greet")
def greet():
    return {"Message":"greet"}

@app.get("/greet/{name}") # path parameter--{name} it dynamically passes the value to the function
#@app.get("/greet/") #to pass everything as query parameter
def greet_name(name:str,age:int,city:Optional[str]=None): #query parameter--age is optional parameter
    #optional to make something optional
    return {"message": f"Hello, {name} {age} {city}"} #f- is for formatted string literal...without it value will not change

class Student(BaseModel): #the core class used to define the structure, types, and constraints of your data
    name:str
    age:int
    roll:int
@app.post("/create_student")
def create_student(student:Student): #student --variable
    return {
        "name":student.name,
        "age":student.age,
        "roll":student.roll
    }