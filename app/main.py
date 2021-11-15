from fastapi import FastAPI
from sqlmodel import SQLModel
from app.ext.db import engine
from app.ext.routes import users
from app.ext.routes import address


app = FastAPI()
app.include_router(users.router)
app.include_router(address.router)

SQLModel.metadata.create_all(engine)
