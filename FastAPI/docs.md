# create virtual environment
```
python -m venv .venv
```

# activate venv
```
source .venv/bin/activate
```

# install dependencies
```
pip install fastapi sqlalchemy uvicorn
```

# run application
```
uvicorn main:app --reload
```

# fastapi provides inbuild docs endpoint
```
localhost:8000/docs
```

# database setup
- to connect to a db - specify the connection string - `sqlite:///users.db`
- to make sqlite work in single thread use `connect_args={"check_same_thread":False}`
- creates a session and base class to create db models/tables
```
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```
- autocomit + autoflush -- to prevent reloading/repopulating data

# database models
- create model classes extending base class by defining required columns and its types for that table
- use `Columns` to define a column with wanted attributes 
```
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    ...
```
- then link the models and engine with `Base.metadata.create_all(engine)`