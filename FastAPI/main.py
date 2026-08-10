from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="Learning FastAPI + SqlAlchemy")

# database setup
engine = create_engine("sqlite:///users.db", connect_args={"check_same_thread":False}) # to make sqlite work in single thread

# autocomit + autoflush -- to prevent reloading data 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# database models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    role = Column(String(50), nullable=False)

# links the models and engine
Base.metadata.create_all(engine)

# endpoints
@app.get("/")
def root():
    return {"message" : "hello from app"}


