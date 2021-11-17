from typing import List
from fastapi import APIRouter
from app.ext.db.users_model import User, UserUpdate, UserRead, UserLogin
from app.ext.controllers import user_controller


router = APIRouter(
    prefix="/users",
    tags=['Users'],
    responses={404: {"description": "Not Found"}},
)

@router.get("/", response_model=List[UserRead])
async def get_user():
    """
    Rota que busca todos os usuários cadastrados.
    """

    users = user_controller.find_users()
    return users


@router.get("/{id}", response_model=List[UserRead])
async def get_user_by_id(id: int):
    """
    Rota que busca um único usuário pelo seu id.
    """

    user = user_controller.find_users_by_id(id)
    return user


@router.patch("/", response_model=UserRead, response_model_exclude_none=True)
async def patch_user(id: int, user: UserUpdate):
    """
    Rota que atualiza os dados de um usuário existente.
    """

    user_controller.update_users(id, user)
    return user


@router.delete("/")
async def delete_user(id: int):
    """
    Rota que deleta um usuário existente.
    """

    return user_controller.remove_users(id)
