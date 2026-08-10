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