from pytest import mark
from unittest.mock import patch
from fastapi import Depends
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.ext.db.users_model import User
from app.ext.controllers.auth_controller import add_user
#from app.ext.providers.hash_provider import generation_hash

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


def test_post_user_deve_retornar_400_quando_ja_existir_um_usuario_com_o_email_passado(
    client: TestClient, session: Session):

    user = User(
        full_name = "Othon breener",
        email = "othon@gmail.com",
        cpf = "366.350.660-63",
        pis = "538.40181.27-3",
        senha = "othon123",
        senha_repet = "othon123")

    session.add(user)
    session.commit()

    user_2 = dict(
        full_name = "Othon breener",
        email = "othon@gmail.com",
        cpf = "501.619.210-35",
        pis = "787.54090.80-5",
        senha = "othon123",
        senha_repet = "othon123")

    data = client.post("/auth/signup", json = user_2, timeout=None)

    assert data.status_code == 400


def test_post_user_deve_retornar_400_quando_ja_existir_um_usuario_com_o_cpf_passado(
    client: TestClient, session: Session):

    user = User(
        full_name = "Othon breener",
        email = "othon@gmail.com",
        cpf = "366.350.660-63",
        pis = "538.40181.27-3",
        senha = "othon123",
        senha_repet = "othon123")

    session.add(user)
    session.commit()

    user_2 = dict(
        full_name = "Othon breener",
        email = "othonbreener@gmail.com",
        cpf = "366.350.660-63",
        pis = "787.54090.80-5",
        senha = "othon123",
        senha_repet = "othon123")

    data = client.post("/auth/signup", json = user_2, timeout=None)

    assert data.status_code == 400


def test_post_user_deve_retornar_400_quando_ja_existir_um_usuario_com_o_pis_passado(
    client: TestClient, session: Session):

    user = User(
        full_name = "Othon breener",
        email = "othon@gmail.com",
        cpf = "366.350.660-63",
        pis = "538.40181.27-3",
        senha = "othon123",
        senha_repet = "othon123")

    session.add(user)
    session.commit()

    user_2 = dict(
        full_name = "Othon breener",
        email = "othonbreener@gmail.com",
        cpf = "501.619.210-35",
        pis = "538.40181.27-3",
        senha = "othon123",
        senha_repet = "othon123")

    data = client.post("/auth/signup", json = user_2, timeout=None)

    assert data.status_code == 400


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


def test_login_user_deve_retornar_200_quando_logar_com_o_email(
    client: TestClient, session: Session):

    user = User(
        full_name = "Othon Breener",
        email = "othon@gmail.com",
        cpf = "299.119.490-10",
        pis = "923.41134.22-0",
        senha = "othon123",
        senha_repet = "othon123")

    add_user(user, session)

    login = dict(email = "othon@gmail.com", senha = "othon123")
    response = client.post('/auth/signin', json = login, timeout=None)

    assert response.status_code == 200


def test_login_user_deve_retornar_200_quando_logar_com_o_cpf(
    client: TestClient, session: Session):

    user = User(
        full_name = "Othon Breener",
        email = "othon@gmail.com",
        cpf = "299.119.490-10",
        pis = "923.41134.22-0",
        senha = "othon123",
        senha_repet = "othon123")

    add_user(user, session)

    login = dict(cpf = "299.119.490-10", senha = "othon123")
    response = client.post('/auth/signin', json = login, timeout=None)

    assert response.status_code == 200


def test_login_user_deve_retornar_200_quando_logar_com_o_pis(
    client: TestClient, session: Session):

    user = User(
        full_name = "Othon Breener",
        email = "othon@gmail.com",
        cpf = "299.119.490-10",
        pis = "923.41134.22-0",
        senha = "othon123",
        senha_repet = "othon123")

    add_user(user, session)

    login = dict(pis = "923.41134.22-0", senha = "othon123")
    response = client.post('/auth/signin', json = login, timeout=None)

    assert response.status_code == 200


def test_login_user_deve_retornar_400_quando_a_senha_estiver_errada(
    client: TestClient, session: Session):

    user = User(
        full_name = "Othon Breener",
        email = "othon@gmail.com",
        cpf = "299.119.490-10",
        pis = "923.41134.22-0",
        senha = "othon123",
        senha_repet = "othon123")

    add_user(user, session)

    login = dict(pis = "923.41134.22-0", senha = "othon")
    response = client.post('/auth/signin', json = login, timeout=None)

    assert response.status_code == 400


def test_login_user_deve_retornar_400_quando_o_pis_estiver_errado(
    client: TestClient, session: Session):

    user = User(
        full_name = "Othon Breener",
        email = "othon@gmail.com",
        cpf = "299.119.490-10",
        pis = "923.41134.22-0",
        senha = "othon123",
        senha_repet = "othon123")

    add_user(user, session)

    login = dict(pis = "923.41134.24-0", senha = "othon123")
    response = client.post('/auth/signin', json = login, timeout=None)

    assert response.status_code == 400


def test_login_user_deve_retornar_400_quando_o_cpf_estiver_errado(
    client: TestClient, session: Session):

    user = User(
        full_name = "Othon Breener",
        email = "othon@gmail.com",
        cpf = "299.119.490-10",
        pis = "923.41134.22-0",
        senha = "othon123",
        senha_repet = "othon123")

    add_user(user, session)

    login = dict(cpf = "299.119.491-10", senha = "othon123")
    response = client.post('/auth/signin', json = login, timeout=None)

    assert response.status_code == 400


def test_login_user_deve_retornar_400_quando_o_email_estiver_errado(
    client: TestClient, session: Session):

    user = User(
        full_name = "Othon Breener",
        email = "othon@gmail.com",
        cpf = "299.119.490-10",
        pis = "923.41134.22-0",
        senha = "othon123",
        senha_repet = "othon123")

    add_user(user, session)

    login = dict(email = "fulano@gmail.com", senha = "othon123")
    response = client.post('/auth/signin', json = login, timeout=None)

    assert response.status_code == 400


def test_auth_me_deve_retornar_200_quando_token_do_usuario_for_valido(
    client: TestClient, session: Session):

    user = User(
        full_name = "Othon Breener",
        email = "othon@gmail.com",
        cpf = "299.119.490-10",
        pis = "923.41134.22-0",
        senha = "othon123",
        senha_repet = "othon123")

    add_user(user, session)

    login = dict(email = "othon@gmail.com", senha = "othon123")
    response_singnin = client.post('/auth/signin', json = login, timeout=None)
    token = response_singnin.json().get('access_token')

    response_me = client.get('/auth/me', headers = {"Authorization": "Bearer " + token})

    assert response_me.status_code == 200


def test_auth_me_deve_retornar_401_quando_o_token_for_invalido(
    client: TestClient):

    response_me = client.get('/auth/me', headers = {"Authorization": "Bearer " + 'batatinha'})

    assert response_me.status_code == 401
