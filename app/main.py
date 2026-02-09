from fastapi import FastAPI
from pydantic import BaseModel

import model/sql_handle.py

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db_tables():
    
