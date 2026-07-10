from sqlalchemy import create_engine #to create the connection to database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#crating database connection

psql_user = "postgres"
psql_password = "root"
psql_host="localhost"
psql_port="5432"
psql_database="fastapi_backendOne"

database_url=f"postgresql://{psql_user}:{psql_password}@{psql_host}:{psql_port}/{psql_database}"


engine=create_engine(database_url)

#session -- when we use api routing session gets created
sessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()

# base
Base=declarative_base() #from declarative_base() we get all the sqlalchemy model

