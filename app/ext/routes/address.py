from typing import List
from fastapi import APIRouter
from app.ext.db.address_model import Address, AddressUpdate
from app.ext.controllers import address_controller

router = APIRouter(
    prefix="/address",
    tags=['Address'],
    responses={404: {"description": "Not Found"}},
)


@router.post("/", response_model=Address, response_model_exclude_none=True)
async def post_address(address: Address):
    """
    Rota que adiciona o endereço de um usuário
    no banco de dados.
    """

    address_controller.add_address(address)
    return address


@router.get("/", response_model=List[Address])
async def get_address():
    """
    Rota que busca todos os endereços cadastrados
    no banco de dados.
    """

    address = address_controller.find_address()
    return address


@router.get("/{id}", response_model=List[Address])
async def get_address_by_id(id: int):
    """
    Rota que busca um endereço específico
    através do seu id.
    """

    address = address_controller.find_address_by_id(id)
    return address


@router.get("/{user_id}", response_model=List[Address])
async def get_address_by_user_id(user_id: int):
    """
    Rota que busca um endereço pelo id do
    usuário no qual ele está relacionado.
    """

    address = address_controller.find_address_by_id_user(user_id)
    return address


@router.patch("/", response_model=AddressUpdate, response_model_exclude_none=True)
async def patch_address(id: int, address: AddressUpdate):
    """
    Rota que atualiza um endereço.
    """

    address_controller.update_address(id, address)
    return address


@router.delete("/")
async def delete_address(id: int):
    """
    Rota que deleta um endereço do banco de dados.
    """

    return address_controller.remove_address(id)
