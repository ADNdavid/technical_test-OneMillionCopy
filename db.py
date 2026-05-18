from typing import Annotated
from sqlmodel import SQLModel, create_engine, Session
from fastapi import Depends, FastAPI
import os

# Configuración para MySQL
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST")
port = os.getenv("MYSQL_PORT")
db_name = os.getenv("MYSQL_DB_NAME")

url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"

# crear el motor que gestionará las sesiones
engine = create_engine(url)

# crear las tablas dentro de la base de datos
def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

def get_session():
    with Session(engine) as session:
        yield session

session_dependency = Annotated[Session, Depends(get_session)]