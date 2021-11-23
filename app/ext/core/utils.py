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
    Função que retorna o cliente assíncrono do httpx.
    """
    with Client(base_url = "http://localhost:8000") as client:
        yield client


def get_session():
    with Session(engine) as session:
        yield session


def get_user_id_by_response(response_session, client: Client):

    bearer = response_session.get('token')
    response = client.get('/auth/me', headers = {'Authorization': 'Bearer ' + bearer})
    data = response.json()
    user_id = data[0].get('id')

    return user_id


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


def creation_session_data(result, client: Client):

    email = result.json()['user'].get('email')
    token = result.json()['access_token']
    response = client.get('/auth/me', headers = {'Authorization': 'Bearer ' + token})
    name = response.json()[0].get('full_name')

    session_data = dict(full_name = name, token = token, email = email)

    return session_data
