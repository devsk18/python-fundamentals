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

# pydantic models
- api model of what we send and recieve - DataClass
- can use it to do form validations

# model responses
- to protect sensitive columns from getting exposed in apis

# establish database
- add a function to create a session of the db

# route decorators
- `@app()` used to define routes and connects its controller function
- configure pydantic response class and status codes along with it

# middleware
- use to intercept request & response
- use async function to not block concurent requests 
- `@app().middleware()` -- fn attached to the route

# db commits
- use `db.commit()` to save new changes
- use `db.refresh()` to reflect the changes

# db queries
- use `db.query(model).filter(col == col).first()/all()` to fetch data with conditions
- use `db.add()` to add a new row
- use `db.delete()` to delete a row