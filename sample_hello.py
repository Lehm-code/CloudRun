from fastapi import FastAPI
from typing import Optional

app = FastAPI()

@app.get("/")
def read_root(last_name: Optional[str] = None, first_name: Optional[str] = None):
    if last_name and first_name:
        return {"message": f"Hello, {last_name} {first_name}! from FastAPI"}
    else:
        return {"message": "Hello, World! from FastAPI"}
