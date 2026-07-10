from auth_database import Base,engine
import models

#create table

Base.metadata.create_all(bind=engine)