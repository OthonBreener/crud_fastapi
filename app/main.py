from fastapi import FastAPI, Request
from sqlmodel import SQLModel
from dotenv import load_dotenv
from app.ext.db import engine
from app.ext.routes import users, address, auth, templates
from fastapi.staticfiles import StaticFiles
#from fastapi.middlewares.core import CORSMiddleware

app = FastAPI()
load_dotenv()
app.mount('/static', StaticFiles(directory='static'), name='static')

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
app.include_router(templates.router)

SQLModel.metadata.create_all(engine)
