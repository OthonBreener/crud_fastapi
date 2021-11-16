from fastapi import HTTPException
from sqlmodel import Session, select
from app.ext.db import engine
from app.ext.db.users_model import User, UserUpdate, UserLogin
from app.ext.providers import hash_provider

def add_user(user: User):
    """
    Método que adiciona um novo usuário no banco de dados.
    """
    user.senha = hash_provider.generation_hash(user.senha)
    user.senha_repet = hash_provider.generation_hash(user.senha_repet)

    user_exist_cpf = find_users_by_cpf(user.CPF)
    if user_exist_cpf:
        raise HTTPException(
                status_code=400,
                detail='Já existe um usuário cadastrado com este cpf.'
            )

    user_exist_pis = find_users_by_pis(user.PIS)
    if user_exist_pis:
        raise HTTPException(
                status_code=400,
                detail='Já existe um usuário cadastrado com este pis.'
            )

    user_exist_email = find_users_by_email(user.email)
    if user_exist_email:
        raise HTTPException(
                status_code=400,
                detail='Já existe um usuário cadastrado com este email.'
            )

    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)


def login(user_login: UserLogin):
    """
    Rota que autentifica um usuário,
    podendo este logar por email, cpf ou pis mais senha.
    """

    senha = user_login.senha
    email = user_login.email
    cpf = user_login.CPF
    pis = user_login.PIS

    user_email = find_users_by_email(email)
    user_cpf = find_users_by_cpf(cpf)
    user_pis = find_users_by_pis(pis)

    if user_email and user_cpf and user_pis is None:
        raise HTTPException(status_code=400, detail='Login ou senha incorretos!')

    if user_email:
        validation_senha =  hash_provider.verification_hash(user_login.senha, user_email[0].senha)

    elif user_cpf:
        validation_senha =  hash_provider.verification_hash(user_login.senha, user_cpf[0].senha)

    else:
        validation_senha =  hash_provider.verification_hash(user_login.senha, user_pis[0].senha)

    if not validation_senha:
        raise HTTPException(status_code=400, detail='Login ou senha incorretos!')

    return user_login


def find_users():
    """
    Função que busca todos os usuários cadastrados no
    banco de dados.
    """

    with Session(engine) as session:
        statement = select(User)
        result = session.exec(statement)
        results = result.all()

    return results


def find_users_by_id(id: int):
    """
    Função que busca um usuario pelo seu id.
    """

    with Session(engine) as session:
        statement = select(User).where(User.id == id)
        result = session.exec(statement)
        results = result.all()

    return results


def find_users_by_cpf(cpf: str):
    """
    Função que busca um usuário pelo cpf.
    """

    with Session(engine) as session:
        statement = select(User).where(User.CPF == cpf)
        result = session.exec(statement)
        results = result.all()

    return results


def find_users_by_pis(pis: str):
    """
    Função que busca um usuário pelo PIS.
    """

    with Session(engine) as session:
        statement = select(User).where(User.PIS == pis)
        result = session.exec(statement)
        results = result.all()

    return results


def find_users_by_email(email: str):
    """
    Função que busca um usuário pelo email.
    """

    with Session(engine) as session:
        statement = select(User).where(User.email == email)
        result = session.exec(statement)
        results = result.all()

    return results


def update_users(id: int, user: UserUpdate):
    """
    Função que atualiza um usuário no banco de dados,
    utilizando o exclude=True para incluir apenas os
    dados enviados na requisição.
    Input:
        id: Id do usuário a ser atualizado
        user: Request com os dados a serem atualizados
    """

    with Session(engine) as session:
        db_user = session.get(User, id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(db_user, key, value)

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user


def remove_users(id: int):
    """
    Função que deleta um usuário do banco de dados.
    """

    with Session(engine) as session:
        statement = select(User).where(User.id == id)
        result = session.exec(statement)
        user = result.one()
        session.delete(user)
        session.commit()

    return "Usuário deletado com sucesso!"
