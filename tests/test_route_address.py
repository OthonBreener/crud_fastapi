from typing import Dict
from pytest import mark
from unittest.mock import patch
from fastapi import Depends
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.ext.db.users_model import User
from app.ext.db.address_model import Address

def add_address_mock(address: Dict[str, str], _ ) -> Dict[str, str]:
    return address

######### usando o mock para mocar o banco de dados ###################

@patch('app.ext.routes.address.address_controller.add_address', new=add_address_mock)
def test_post_address_deve_retornar_422_quando_o_dado_de_entrada_possuir_um_tipo_invalido(client: TestClient) -> None:

    address = dict(
        cep = {"ola pessoas":"hello"},
        country = "Brasil",
        state = "MG",
        city = "Ibia",
        street = "54",
        number = "87",
        complement = "Qualquer"
    )

    user = dict(
        full_name = "Othon breener",
        email = "othon@gmail.com",
        cpf = "366.350.660-63",
        pis = "538.40181.27-3",
        senha = "othon123",
        senha_repet = "othon123"
        )

    response_user = client.post("/auth/singnup", json=user, timeout=None)
    response = client.post("/address/register", json=address, timeout=None)

    assert response.status_code == 422


@patch('app.ext.routes.address.address_controller.add_address', new=add_address_mock)
def test_post_address_deve_retornar_200_e_os_mesmo_dados_de_entrada(
    client: TestClient,
    session: Session
    ) -> None:

    params = dict(
        cep = "38950000",
        country = "Brasil",
        state = "MG",
        city = "Ibia",
        street = "54",
        number = "87",
        complement = "Qualquer",
        user_id = 14)

    datas_user_fake = dict(
        full_name = "Othon breener",
        email = "othon@gmail.com",
        cpf = "366.350.660-63",
        pis = "538.40181.27-3",
        senha = "othon123",
        senha_repet = "othon123")

    response_user = client.post("/auth/singnup", json=datas_user_fake, timeout=None)

    response = client.post("/address/register", json=params, timeout=None)
    data = response.json()

    assert response.status_code == 200
    assert data["country"] == "Brasil"
    assert data["state"] == "MG"
    assert data["cep"] == "38950000"
    assert data["city"] == "Ibia"
    assert data["street"] == "54"
    assert data["number"] == "87"
    assert data["complement"] == "Qualquer"
    assert data["user_id"] == 14


@patch('app.ext.routes.address.address_controller.add_address', new=add_address_mock)
def test_post_address_deve_retornar_200_quando_o_id_do_usuario_nao_for_passado(client: TestClient) -> None:

    address = dict(
        cep = "38950000",
        country = "Brasil",
        state = "MG",
        city = "Ibia",
        street = "54",
        number = "87",
        complement = "Qualquer"
        )

    response = client.post("/address/register", json=address, timeout=None)
    print(response.json())
    assert response.status_code == 200


############ Utilizando um banco de dados fake ######################

def test_get_addres_deve_retorna_200(client: TestClient, session: Session) -> None:

    user = User(
        full_name = "Othon breener",
        email = "othon@gmail.com",
        cpf = "366.350.660-63",
        pis = "538.40181.27-3",
        senha = "othon123",
        senha_repet = "othon123")

    session.add(user)
    session.commit()

    response = client.get("/address/register")
    data = response.json()

    assert response.status_code == 200


def test_get_addres_id_deve_retorna_200_quando_existir_um_cadastro_com_o_id_passado(
    client: TestClient,
    session: Session) -> None:

    address = Address(
        cep = "38950-000",
        country = "Brasil",
        state = "MG",
        city = "Ibia",
        street = "54",
        number = "87",
        complement = "Qualquer"
        )

    session.add(address)
    session.commit()

    response = client.get("/address/register/1")
    data = response.json()

    assert response.status_code == 200
    assert type(data) == list
    assert type(data[0]) == dict


def test_get_addres_id_deve_retorna_404_quando_nao_existir_um_cadastro_com_o_id_passado(
    client: TestClient,
    session: Session
    ) -> None:

    response = client.get("/address/register/40")
    assert response.status_code == 404


def test_get_address_by_user_id_deve_retornar_200_quando_buscar_um_endereco_pelo_id_do_usuario(
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

    address = Address(
        cep = "38950-000",
        country = "Brasil",
        state = "MG",
        city = "Ibia",
        street = "54",
        number = "87",
        complement = "Qualquer",
        user_id = 1
        )

    session.add(address)
    session.commit()

    response = client.get("/address/register/get_user_id/1")
    assert response.status_code == 200


def test_get_address_by_user_id_deve_retornar_404_quando_nao_encontrar_um_endereco_com_o_id_de_usuario_passado(
    client: TestClient,
    session: Session) -> None:

    address = Address(
        cep = "38950-000",
        country = "Brasil",
        state = "MG",
        city = "Ibia",
        street = "54",
        number = "87",
        complement = "Qualquer",
        user_id = 1
        )

    session.add(address)
    session.commit()

    response = client.get("/address/register/get_user_id/5")
    assert response.status_code == 404


def test_post_address_deve_retornar_422_quando_algum_dado_obrigatorio_estiver_faltando(
    client: TestClient,
    session: Session
    ) -> None:

    params = dict(
        country = "Brasil",
        state = "MG",
        city = "Ibia",
        street = "54",
        number = "87",
        complement = "Qualquer"
        )

    response = client.post("/address/register", json=params, timeout=None)
    assert response.status_code == 422

def test_post_address_deve_retornar_422_se_o_cep_nao_tiver_o_tamanho_certo(
    client: TestClient
    ) -> None:

    params = dict(
        cep = "389000",
        country = "Brasil",
        state = "MG",
        city = "Ibia",
        street = "54",
        number = "87",
        complement = "Qualquer"
        )

    response = client.post("/address/register", json=params)
    assert response.status_code == 422


def test_post_address_no_banco_fake_deve_retornar_200(
    client: TestClient,
    session: Session
    ) -> None:

    address = dict(
        cep = "38950-000",
        country = "Brasil",
        state = "MG",
        city = "Ibia",
        street = "54",
        number = "87",
        complement = "Qualquer")

    response = client.post("/address/register", json = address, timeout=None)
    assert response.status_code == 200


def test_post_address_no_banco_fake_deve_retornar_422_quando_o_estiver_faltando_dados(
    client: TestClient
    ) -> None:

    params = dict(
        cep = "38408108",
        state = "MG",
        city = "Uberlandia",
        street = "tomas falbo",
        number = "906",
        complement = "Apt 202")

    response = client.post("/address/register", json=params, timeout=None)
    assert response.status_code == 422


def test_post_address_no_banco_fake_deve_retornar_422_quando_os_dados_nao_tiverem_o_tamanho_certo(
    client: TestClient
    ) -> None:

    address = dict(
        cep = "38408108",
        state = "M",
        city = "U",
        street = "tomas falbo",
        number = "906",
        complement = "Apt 202")

    response = client.post("/address/register", json=address, timeout=None)
    assert response.status_code == 422


def test_patch_address_deve_retornar_200_quando_os_dados_forem_atualizados_com_sucesso(
    client: TestClient,
    session: Session) -> None:

    address = Address(
        country = "Brasil",
        cep = "38408108",
        state = "MG",
        city = "Uberlandia",
        street = "tomas falbo",
        number = "906",
        complement = "Apt 202")

    session.add(address)
    session.commit()

    address_update = dict(city = "Uberaba")

    response = client.patch("/address/register/update/1", json=address_update)
    data = response.json()

    assert response.status_code == 200
    assert data["city"] == "Uberaba"


def test_patch_address_deve_retornar_404_quando_os_dados_nao_existirem_para_o_id_passado(
    client: TestClient) -> None:

    address_update = dict(city = "Uberaba")

    response = client.patch("/address/register/update/1", json=address_update)
    data = response.json()

    assert response.status_code == 404


def test_delete_address_deve_retornar_404_quando_nao_existir_dados_para_o_id_passado(
    client: TestClient) -> None:

    response = client.delete("/address/register/delete/1")
    assert response.status_code == 404


def test_delete_address_deve_retornar_200_quando_os_dados_forem_deletados_com_sucesso(
    client: TestClient,
    session: Session) -> None:

    address = Address(
        country = "Brasil",
        cep = "38408108",
        state = "MG",
        city = "Uberlandia",
        street = "tomas falbo",
        number = "906",
        complement = "Apt 202")

    session.add(address)
    session.commit()

    response = client.delete("/address/register/delete/1")
    assert response.status_code == 200
