from sqlalchemy import Column,Integer,String
from auth_database import Base

#database structure

class User(Base):
    __tablename__="Users"

    id=Column(Integer,primary_key=True,index=True)
    username=Column(String(255),unique=True,index=True)
    email=Column(String(255),unique=True,index=True)
    hashed_password=Column(String(255))
    role=Column(String(50),default="User") #default role is user