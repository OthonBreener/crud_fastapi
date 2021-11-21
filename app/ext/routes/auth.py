from typing import List
from fastapi import APIRouter, Depends
from app.ext.db.users_model import User, UserUpdate, UserRead, UserLogin, UserLoginSucess
from app.ext.controllers import auth_controller


router = APIRouter(
    prefix="/auth",
    tags=['Auth'],
    responses={404: {"description": "Not Found"}},
)

@router.post("/signup", response_model=UserRead)
async def post_user(user: User):
    """
    Rota que adiciona um novo usuário.
    Rota Signup
    """
    auth_controller.add_user(user)
    return user


@router.post("/signin",
    response_model=UserLoginSucess,
    response_model_exclude_none=True
)
async def login_user(user_login: UserLogin):
    """
    Rota que loga o usuário no sistema.
    """

    return auth_controller.login(user_login)


@router.get("/me", response_model=List[UserRead])
def me(user: User = Depends(auth_controller.find_user_active_section)):
    """
    Rota que verifica se o usuário está devidamente logado.
    """
    return user
