from pytest import mark
from unittest.mock import patch
from fastapi import Depends
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.ext.db.users_model import User


def test_get_user_deve_retornar_200(
    client: TestClient,
    session: Session
    ) -> None:

    response = client.get("/users/get")
    assert response.status_code == 200


def test_get_user_id_deve_retornar_404_quando_nao_existir_um_user_com_o_id(
    client: TestClient,
    session: Session
    ) -> None:

    response = client.get("/users/get/40")
    assert response.status_code == 404


def test_get_user_id_deve_retornar_200_quando_existir_um_user_com_o_id(
    client: TestClient,
    session: Session
    ) -> None:

    user = User(
        full_name = "Othon breener",
        email = "othon@gmail.com",
        cpf = "366.350.660-63",
        pis = "538.40181.27-3",
        senha = "othon123",
        senha_repet = "othon123"
    )
    session.add(user)
    session.commit()

    response = client.get("/users/get/1")

    assert response.status_code == 200


def test_patch_user_deve_retornar_200_quando_os_dados_forem_atualizados_com_sucesso(
    client:TestClient,
    session: Session) -> None:

    user = User(
        full_name = "Othon breener",
        email = "othon@gmail.com",
        cpf = "366.350.660-63",
        pis = "538.40181.27-3",
        senha = "othon123",
        senha_repet = "othon123"
    )
    session.add(user)
    session.commit()

    user_update = dict(full_name = "Othon Marques")

    response = client.patch("/users/patch/update/1", json=user_update)
    data = response.json()

    assert response.status_code == 200
    assert data["full_name"] == "Othon Marques"


def test_patch_user_deve_retornar_404_quando_nao_existir_um_usuario_com_o_id_passado(
    client:TestClient,
    session: Session) -> None:

    user_update = dict(full_name = "Othon Marques")

    response = client.patch("/users/patch/update/1", json=user_update)
    data = response.json()

    assert response.status_code == 404


def test_delete_user_deve_retornar_404_quando_o_usuario_nao_existir(
    client: TestClient
    ) -> None:

    response = client.delete("/users/delete/5")

    assert response.status_code == 404


def test_delete_user_deve_retornar_200_quando_deletar_um_usuario_com_sucesso(
    client: TestClient,
    session: Session
    ) -> None:

    user = User(
        full_name = "Othon breener",
        email = "othon@gmail.com",
        cpf = "366.350.660-63",
        pis = "538.40181.27-3",
        senha = "othon123",
        senha_repet = "othon123"
    )
    session.add(user)
    session.commit()

    response = client.delete("/users/delete/1")

    assert response.status_code == 200
