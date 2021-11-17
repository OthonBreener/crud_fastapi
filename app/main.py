from fastapi import FastAPI
from fastapi.templating import Jinja2Template
from sqlmodel import SQLModel
from dotenv import load_dotenv
from app.ext.db import engine
from app.ext.routes import users
from app.ext.routes import address
from app.ext.routes import auth
#from fastapi.middlewares.core import CORSMiddleware

app = FastAPI()
load_dotenv()
templates = Jinja2Template(directory='templates')
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
app.include_router(auth.router)

SQLModel.metadata.create_all(engine)
