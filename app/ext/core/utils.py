import os
from sqlmodel import Session
from httpx import Client
from typing import Dict
from validate_docbr import PIS, CPF
from app.ext.db import engine

def get_env(data: str):
    """
    Função que busca uma string nas váriaveis de ambiente.
    """
    return os.environ.get(data)


def get_client():
    """
    Função que retorna o cliente do httpx.
    """
    with Client(base_url = "http://localhost:8000") as client:
        yield client


def get_session():
    with Session(engine) as session:
        yield session


def verification_type_login(username: str, password: str) -> Dict[str, str]:

    cpf = CPF()
    if cpf.validate(username) is True:
        login = dict(cpf = username, senha = password)

    pis = PIS()
    if pis.validate(username) is True:
        login = dict(pis = username, senha = password)

    else:
        login = dict(email = username, senha = password)

    return login


def creation_session_data(token: str, client: Client):
    """
    Função que cria cookies armazenando
    o token do usuário.
    """
    session_data = dict(token = token)
    response_session = client.post('/session/create_session', json = session_data)

    return response_session
