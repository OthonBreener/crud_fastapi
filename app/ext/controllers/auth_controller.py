from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlmodel import Session, select
from validate_docbr import PIS, CPF
from app.ext.db.users_model import User, UserLogin, UserLoginSucess
from app.ext.providers import hash_provider, token_provider
from app.ext.controllers import user_controller
from app.ext.core.utils import get_session

oauth2_schema = OAuth2PasswordBearer(tokenUrl = 'token')


def add_user(user: User, session: Session):
    """
    Método que adiciona um novo usuário no banco de dados.
    """
    user.senha = hash_provider.generation_hash(user.senha)
    user.senha_repet = hash_provider.generation_hash(user.senha_repet)

    user_exist_cpf = user_controller.find_users_by_cpf(user.cpf, session)
    if user_exist_cpf:
        raise HTTPException(
                status_code=400,
                detail='Já existe um usuário cadastrado com este cpf.'
            )

    user_exist_pis = user_controller.find_users_by_pis(user.pis, session)
    if user_exist_pis:
        raise HTTPException(
                status_code=400,
                detail='Já existe um usuário cadastrado com este pis.'
            )

    user_exist_email = user_controller.find_users_by_email(user.email, session)
    if user_exist_email:
        raise HTTPException(
                status_code=400,
                detail='Já existe um usuário cadastrado com este email.'
            )

    session.add(user)
    session.commit()
    session.refresh(user)


def login(user_login: UserLogin, session: Session):
    """
    Rota que autentifica um usuário,
    podendo este logar por email, cpf ou pis mais senha.
    """

    senha = user_login.senha
    email = user_login.email
    cpf = user_login.cpf
    pis = user_login.pis

    user_email = user_controller.find_users_by_email(email, session)
    user_cpf = user_controller.find_users_by_cpf(cpf, session)
    user_pis = user_controller.find_users_by_pis(pis, session)

    if user_email:
        validation_senha =  hash_provider.verification_hash(user_login.senha, user_email[0].senha)
        token = token_provider.creation_access_token({'sub':user_email[0].email})

    elif user_cpf:
        validation_senha =  hash_provider.verification_hash(user_login.senha, user_cpf[0].senha)
        token = token_provider.creation_access_token({'sub':user_cpf[0].cpf})

    else:
        validation_senha =  hash_provider.verification_hash(user_login.senha, user_pis[0].senha)
        token = token_provider.creation_access_token({'sub':user_pis[0].pis})

    if not validation_senha:
        raise HTTPException(status_code=400, detail='Login ou senha incorretos!')

    return UserLoginSucess(user=user_login, access_token=token)


def find_user_active_section(
    token: str = Depends(oauth2_schema),
    session: Session = Depends(get_session),
    ):
    """
    Função responsável por decodificar um token jwt e pegar o dado
    de login (variando entre email, cpf e pis), com esse dado validado,
    buscar um usuário no banco de dados e retorna-lo.
    """
    exception = HTTPException(status_code=401, detail='Token Inválido!')

    try:
        data_login = token_provider.validation_access_token(token)
    except JWTError:
        raise exception

    if not data_login:
        raise exception

    cpf = CPF()
    if cpf.validate(data_login) is True:

        user_cpf = user_controller.find_users_by_cpf(data_login, session)
        if not user_cpf:
            raise exception
        return user_cpf

    pis = PIS()
    if pis.validate(data_login) is True:
        user_pis = user_controller.find_users_by_pis(data_login, session)
        if not user_pis:
            raise exception
        return user_pis

    else:
        user_email = user_controller.find_users_by_email(data_login, session)
        if not user_email:
            raise exception
        return user_email
