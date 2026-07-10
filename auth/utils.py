#for hashing password

from passlib.context import CryptContext
password_context=CryptContext(schemes=["argon2"],deprecated="auto")

def hash_password(password:str)->str: #output is also string
    return password_context.hash(password)

def verify_password(plain_password:str,hashed_password:str)->bool:
    return password_context.verify(plain_password,hashed_password)