from auth.auth_database import Base,engine
from auth import models

#create table

Base.metadata.create_all(bind=engine)