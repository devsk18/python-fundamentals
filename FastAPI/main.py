from fastapi import FastAPI, HTTPException, Depends, status, Request
from sqlalchemy import create_engine, Column, Integer, String

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from pydantic import BaseModel, Field, EmailStr
from typing import List

import time

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

# pydantic models (Dataclass) - api models we send & recieve
class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    role: str = Field(min_length=2, max_length=100)

# helps to protect private datas of model class - restrict in api response
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Configs:
        from_attributes = True


# to establish the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

get_db()

# middlewares
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    log_message = f"{request.method} {request.url} completed in {process_time:.4f} secs"
    print(log_message)
    return response

# endpoints
@app.get("/")
def root():
    return {"message":"Hello from root"}

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user

@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists!")

    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    for field, value in user.model_dump().items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    db.delete(db_user)
    db.commit()
    return {"message":"user deleted"}

@app.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()