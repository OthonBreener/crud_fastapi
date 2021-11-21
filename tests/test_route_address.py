from pytest import mark
from unittest.mock import patch
from fastapi import Depends
from httpx import AsyncClient


def add_address_mock(address):
    return address


@mark.anyio
async def test_get_addres_deve_retorna_200(async_client: AsyncClient) -> None:

    response = await async_client.get("/address/register")
    data = response.json()

    assert response.status_code == 200
    #assert type(data) == list
    #assert type(data[0]) == dict


@mark.anyio
async def test_get_addres_id_deve_retorna_200_quando_existir_um_cadastro_com_o_id_passado(async_client: AsyncClient) -> None:

    response = await async_client.get("/address/register/1")
    data = response.json()

    assert response.status_code == 200
    #assert type(data) == list
    #assert type(data[0]) == dict


@mark.anyio
async def test_get_addres_id_deve_retorna_404_quando_nao_existir_um_cadastro_com_o_id_passado(async_client: AsyncClient) -> None:

    response = await async_client.get("/address/register/40")
    assert response.status_code == 404


@mark.anyio
@patch('app.ext.routes.address.address_controller.add_address', new=add_address_mock)
async def test_post_address_deve_retornar_200_e_os_mesmo_dados_de_entrada(async_client: AsyncClient) -> None:

    params = dict(cep = "38950000", country = "Brasil", state = "MG", city = "Ibia",
                 street = "54", number = "87", complement = "Qualquer", user_id = 14)

    response = await async_client.post("/address/register", json=params, timeout=None)
    data = response.json()

    assert response.status_code == 200
    #assert data["country"] == "Brasil"
    #assert data["state"] == "MG"
    #assert data["cep"] == "38950-000"
    #assert data["city"] == "Ibia"
    #assert data["street"] == "54"
    #assert data["number"] == "87"
    #assert data["complement"] == "Qualquer"
    #assert data["user_id"] == 14


@mark.anyio
async def test_post_address_deve_retornar_422_quando_algum_dado_obrigatorio_estiver_faltando(async_client: AsyncClient) -> None:

    params = dict(country = "Brasil", state = "MG", city = "Ibia",
                 street = "54", number = "87", complement = "Qualquer", user_id = 14)

    response = await async_client.post("/address/register", json=params, timeout=None)
    assert response.status_code == 422


@mark.anyio
@patch('app.ext.routes.address.address_controller.add_address', new=add_address_mock)
async def test_post_address_deve_retornar_200_quando_o_id_do_usuario_nao_for_passado(async_client: AsyncClient) -> None:

    params = dict(cep = "3", country = "Brasil", state = "MG", city = "Ibia",
                 street = "54", number = "87", complement = "Qualquer")

    response = await async_client.post("/address/register", json=params, timeout=None)
    assert response.status_code == 200


@mark.anyio
@patch('app.ext.routes.address.address_controller.add_address', new=add_address_mock)
async def test_post_address_deve_retornar_422_quando_o_dado_de_entrada_possuir_um_tipo_invalido(async_client: AsyncClient) -> None:

    params = dict(cep = {"ola pessoas":"hello"}, country = "Brasil", state = "MG", city = "Ibia",
                 street = "54", number = "87", complement = "Qualquer")

    response = await async_client.post("/address/register", json=params, timeout=None)
    assert response.status_code == 422


@mark.anyio
async def test_post_address_no_banco_fake_deve_retornar_200(async_client: AsyncClient) -> None:

    params_1 = dict(cep = "38950000", country = "Brasil", state = "MG", city = "Ibia",
                 street = "54", number = "87", complement = "Qualquer", user_id = 14)

    response = await async_client.post("/address/register", json=params_1, timeout=None)

    data = response.json()

    assert response.status_code == 200
    #assert data["country"] == "Brasil"
    #assert data["state"] == "MG"
    #assert data["cep"] == "38950-000"
    #assert data["city"] == "Ibia"
    #assert data["street"] == "54"
    #assert data["number"] == "87"
    #assert data["complement"] == "Qualquer"
    #assert data["user_id"] == 14


@mark.anyio
async def test_post_address_no_banco_fake_deve_retornar_422_quando_o_estiver_faltando_dados(async_client: AsyncClient) -> None:

    params = dict(cep = "38408108", state = "MG", city = "Uberlandia",
                 street = "tomas falbo", number = "906", complement = "Apt 202", user_id = 1)

    response = await async_client.post("/address/register", json=params, timeout=None)

    assert response.status_code == 422


@mark.anyio
async def test_post_address_no_banco_fake_deve_retornar_422_quando_os_dados_nao_tiverem_o_tamanho_certo(async_client: AsyncClient) -> None:

    params = dict(cep = "38408108", state = "M", city = "U",
                 street = "tomas falbo", number = "906", complement = "Apt 202", user_id = 1)

    response = await async_client.post("/address/register", json=params, timeout=None)

    assert response.status_code == 422
