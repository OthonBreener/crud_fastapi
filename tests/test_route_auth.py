from pytest import mark
from unittest.mock import patch
from fastapi import Depends
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.ext.db.users_model import User


def test_post_user_deve_retornar_200(client: TestClient):

    user = dict(
        full_name = "Othon breener",
        email = "othon@gmail.com",
        cpf = "366.350.660-63",
        pis = "538.40181.27-3",
        senha = "othon123",
        senha_repet = "othon123")

    response = client.post("/auth/signup", json = user, timeout=None)

    assert response.status_code == 200


def test_post_user_deve_retornar_422_quando_estiver_faltando_dados(client: TestClient):

    user = dict(
        email = "othon@gmail.com",
        cpf = "366.350.660-63",
        pis = "538.40181.27-3",
        senha = "othon123",
        senha_repet = "othon123")

    response = client.post("/auth/signup", json = user, timeout=None)

    assert response.status_code == 422


def test_post_user_deve_retornar_422_quando_o_nome_nao_estiver_completo(client: TestClient):

    user = dict(
        full_name = "Othon",
        email = "othon@gmail.com",
        cpf = "366.350.660-63",
        pis = "538.40181.27-3",
        senha = "othon123",
        senha_repet = "othon123")

    response = client.post("/auth/signup", json = user, timeout=None)
    assert response.status_code == 422


def test_post_user_deve_retornar_422_quando_os_dados_forem_invalidos(client: TestClient):

    user = dict(
        full_name = {"first_name":"Othon", "last_name":"Breener"},
        email = "othon@gmail.com",
        cpf = "366.350.660-63",
        pis = "538.40181.27-3",
        senha = "othon123",
        senha_repet = "othon123")

    response = client.post("/auth/signup", json = user, timeout=None)
    assert response.status_code == 422


def test_post_user_deve_retornar_422_quando_o_cpf_for_invalido(client: TestClient):

    user = dict(
        full_name = {"first_name":"Othon", "last_name":"Breener"},
        email = "othon@gmail.com",
        cpf = "366.350.660-61",
        pis = "538.40181.27-3",
        senha = "othon123",
        senha_repet = "othon123")

    response = client.post("/auth/signup", json = user, timeout=None)
    assert response.status_code == 422


def test_post_user_deve_retornar_422_quando_o_pis_for_invalido(client: TestClient):

    user = dict(
        full_name = {"first_name":"Othon", "last_name":"Breener"},
        email = "othon@gmail.com",
        cpf = "366.350.660-63",
        pis = "538.40181.27-0",
        senha = "othon123",
        senha_repet = "othon123")

    response = client.post("/auth/signup", json = user, timeout=None)
    assert response.status_code == 422
