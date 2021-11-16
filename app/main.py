from fastapi import FastAPI
from sqlmodel import SQLModel
from app.ext.db import engine
from app.ext.routes import users
from app.ext.routes import address
#from fastapi.middlewares.core import CORSMiddleware

app = FastAPI()

# CORS - Para caso de aplicação com JS

"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""

app.include_router(users.router)
app.include_router(address.router)

SQLModel.metadata.create_all(engine)
