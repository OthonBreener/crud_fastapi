from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.ext.db.address_model import Address, AddressUpdate, AddressRead
from app.ext.controllers import address_controller
from app.ext.core.utils import get_session


router = APIRouter(
    prefix="/address",
    tags=['Address'],
    responses={404: {"description": "Not Found"}},
)


@router.post("/register", response_model=AddressRead, response_model_exclude_none=True)
def post_address(address: Address,  session: Session = Depends(get_session)):
    """
    Rota que adiciona o endereço de um usuário
    no banco de dados.
    """

    address_controller.add_address(address, session)
    return address


@router.get("/register", response_model=List[Address])
def get_address(session: Session = Depends(get_session)):
    """
    Rota que busca todos os endereços cadastrados
    no banco de dados.
    """

    address = address_controller.find_address(session)
    return address


@router.get("/register/{id}", response_model=List[Address])
def get_address_by_id(id: int, session: Session = Depends(get_session)):
    """
    Rota que busca um endereço específico
    através do seu id.
    """

    address = address_controller.find_address_by_id(id, session)
    return address


@router.get("/register/{user_id}", response_model=List[Address])
def get_address_by_user_id(user_id: int, session: Session = Depends(get_session)):
    """
    Rota que busca um endereço pelo id do
    usuário no qual ele está relacionado.
    """

    address = address_controller.find_address_by_id_user(user_id, session)
    return address


@router.patch("/register/update/", response_model=AddressUpdate, response_model_exclude_none=True)
def patch_address(id: int, address: AddressUpdate, session: Session = Depends(get_session)):
    """
    Rota que atualiza um endereço.
    """

    address_controller.update_address(id, address, session)
    return address


@router.delete("/register")
def delete_address(id: int, session: Session = Depends(get_session)):
    """
    Rota que deleta um endereço do banco de dados.
    """

    return address_controller.remove_address(id, session)
