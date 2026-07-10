#need to import pydantic models that we will use

from pydantic import BaseModel, EmailStr

#schemas for new user creation and login
class userCreate(BaseModel):
    username:str
    email:str
    password:str
    role:str

#for existing user login
class userLogin(BaseModel):
    username:str
    password:str