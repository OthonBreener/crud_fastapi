from fastapi import HTTPException
from sqlmodel import Session, select
from app.ext.db import engine
from app.ext.db.users_model import User, UserUpdate


def add_user(user: User):
    """
    Método que adiciona um novo usuário no banco de dados.
    """

    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)


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

        #import ipdb; ipdb.set_trace()

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
