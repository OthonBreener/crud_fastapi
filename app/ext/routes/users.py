from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.ext.db.users_model import User, UserUpdate, UserRead, UserLogin
from app.ext.controllers import user_controller
from app.ext.core.utils import get_session

router = APIRouter(
    prefix="/users",
    tags=['Users'],
    responses={404: {"description": "Not Found"}},
)

@router.get("/get", response_model=List[UserRead])
def get_user(session: Session = Depends(get_session)):
    """
    Rota que busca todos os usuários cadastrados.
    """

    users = user_controller.find_users(session)
    return users


@router.get("/get/{id}", response_model=List[UserRead])
def get_user_by_id(id: int, session: Session = Depends(get_session)):
    """
    Rota que busca um único usuário pelo seu id.
    """

    user = user_controller.find_users_by_id(id, session)
    return user


@router.patch("/patch/update/{id}", response_model=UserRead, response_model_exclude_none=True)
def patch_user(id: int, user: UserUpdate, session: Session = Depends(get_session)):
    """
    Rota que atualiza os dados de um usuário existente.
    """

    user_controller.update_users(id, user, session)
    return user


@router.delete("/delete/{id}")
def delete_user(id: int, session: Session = Depends(get_session)):
    """
    Rota que deleta um usuário existente.
    """

    return user_controller.remove_users(id, session)
