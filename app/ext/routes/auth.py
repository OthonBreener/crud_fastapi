from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.ext.db.users_model import User, UserUpdate, UserRead, UserLogin, UserLoginSucess
from app.ext.controllers import auth_controller
from app.ext.core.utils import get_session

router = APIRouter(
    prefix="/auth",
    tags=['Auth'],
    responses={404: {"description": "Not Found"}},
)

@router.post("/signup", response_model=UserRead)
def post_user(user: User, session: Session = Depends(get_session)):
    """
    Rota que adiciona um novo usuário.
    Rota Signup
    """
    auth_controller.add_user(user, session)
    return user


@router.post("/signin",
    response_model=UserLoginSucess,
    response_model_exclude_none=True
)
def login_user(user_login: UserLogin, session: Session = Depends(get_session)):
    """
    Rota que loga o usuário no sistema.
    """

    return auth_controller.login(user_login, session)


@router.get("/me", response_model=List[UserRead])
def me(
    user: User = Depends(auth_controller.find_user_active_section),
    session: Session = Depends(get_session)
    ):
    """
    Rota que verifica se o usuário está devidamente logado.
    """
    return user
