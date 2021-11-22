import os
from httpx import Client
from sqlmodel import Session
from app.ext.db import engine


def get_env(data: str):
    """
    Função que busca uma string nas váriaveis de ambiente.
    """
    return os.environ.get(data)


def get_client():
    """
    Função que retorna o cliente assíncrono do httpx.
    """
    with Client(base_url = "http://localhost:8000") as client:
        yield client


def get_session():
    with Session(engine) as session:
        yield session
