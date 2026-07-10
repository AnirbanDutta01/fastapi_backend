from fastapi import FastAPI,Depends,HTTPException,status
from sqlalchemy.orm import Session
import models, schema, utils
from auth_database import get_db
from jose import jwt
from datetime import datetime,timedelta
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer #to simplify extraction of login credentials and parse it
from jose import JWTError

secret_key="3_6-yTC2-Pnp4_dh6ZIMfvKi_phblha8AN1hhnHbs5I"
ALGORITHM="HS256" #the algorithm used to generate the jwt token
access_token_expiry_minutes=30 #when user login then the access token will be valid for 30 minutes

#helper function that takes user data and generates jwt token
def create_access_token(data:dict): #user role,password all comes in dictionary form
    to_encode=data.copy() #copying the data to another variable
    expire_time=datetime.utcnow() + timedelta(minutes=access_token_expiry_minutes) #adding 30 minutes to the current time
    to_encode.update({"exp": expire_time}) #updating the dictionary with expiry time
    encode_jwt=jwt.encode(to_encode,secret_key,algorithm=ALGORITHM) #encoding the data with secret key and algorithm
    return encode_jwt

app=FastAPI()

@app.post("/signup")    #schema.user create taken from schema
def register_user(user:schema.userCreate,db:Session=Depends(get_db)):
    #check if user exists or not
    existing_user=db.query(models.User).filter(models.User.username==user.username).first() #models taken from models.py
    if existing_user:
        raise HTTPException(status_code=400,detail="user already exists")
    
    #hash the password
    hashed_pass=utils.hash_password(user.password) #from utils.py it is taken
    
    #create new user instance
    new_user=models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pass,
        role=user.role
    )

    #save user to db
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    #return value excluding password

    return {"id":new_user.id,"user_name":new_user.username,"email":new_user.email,"role":new_user.role}

#creating loggedin endpoint
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db) ):
    user=db.query(models.User).filter(models.User.username==form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Username")
    
    if not utils.verify_password(form_data.password,user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,details="invalid password")
    
    token_data={'sub':user.username,'role':user.role}
    token=create_access_token(token_data)
    return{"access_token":token,"token_type":"bearer"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token:str=Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate credential",headers={"WWW-Authenticate":"Bearer"})

    try:
        payload=jwt.decode(token,secret_key,algorithms=ALGORITHM)
        username:str=payload.get("sub")
        role:str =payload.get("role")
        if username is None or role is None:
            raise credential_exception
        
    except JWTError:
        raise credential_exception
    
    return {"username":username,"role":role}

@app.get("/protected")
def protected_route(current_user:dict=Depends(get_current_user)):
    return {"message":f"Hello {current_user['username']}" | "You accessed a protected route"}

def require_roles(allowed_roles: list[str]):
    def role_checker(current_user:dict=Depends(get_current_user)):
        user_role=current_user.get("role")
        if user_role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not enough permissions")
        
        return current_user
    return role_checker

@app.get("/profile")
def profile(current_user:dict = Depends(require_roles(["user","admin"]))):
    return {"message":f"profile of {current_user['username']} with role {current_user['role']}"}

@app.get("/user/dashboard")
def user_dashboard(current_user:dict=Depends(require_roles(["user"]))):
    return {"message":f"welcome user"}

@app.get("/admin/dashboard")
def admin_dashboard(current_user:dict=Depends(require_roles(["admin"]))):
    return {"message":f"welcome admin"}