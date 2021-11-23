from fastapi import HTTPException
from sqlmodel import Session, select
from app.ext.db.users_model import User, UserUpdate, UserLogin


def find_users(session: Session):
    """
    Função que busca todos os usuários cadastrados no
    banco de dados.
    """

    statement = select(User)
    result = session.exec(statement)
    results = result.all()

    return results


def find_users_by_id(id: int, session: Session):
    """
    Função que busca um usuario pelo seu id.
    """

    statement = select(User).where(User.id == id)
    result = session.exec(statement)
    results = result.all()
    if not results:
        raise HTTPException(status_code=404, detail="User not found")

    return results


def find_users_by_cpf(cpf: str, session: Session):
    """
    Função que busca um usuário pelo cpf.
    """

    statement = select(User).where(User.cpf == cpf)
    result = session.exec(statement)
    results = result.all()

    return results


def find_users_by_pis(pis: str, session: Session):
    """
    Função que busca um usuário pelo PIS.
    """

    statement = select(User).where(User.pis == pis)
    result = session.exec(statement)
    results = result.all()

    return results


def find_users_by_email(email: str, session: Session):
    """
    Função que busca um usuário pelo email.
    """

    statement = select(User).where(User.email == email)
    result = session.exec(statement)
    results = result.all()

    return results


def find_user_and_password(email: str, session: Session):
    """
    Função que busca o password do user
    para confirmar o delete na rota de template.
    """

    statement = select(User).where(User.email == email)
    result = session.exec(statement)
    results = result.all()

    return results


def update_users(id: int, user: UserUpdate, session: Session) -> UserUpdate:
    """
    Função que atualiza um usuário no banco de dados,
    utilizando o exclude=True para incluir apenas os
    dados enviados na requisição.
    Input:
        id: Id do usuário a ser atualizado
        user: Request com os dados a serem atualizados
    """

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


def remove_users(id: int, session: Session):
    """
    Função que deleta um usuário do banco de dados.
    """

    statement = session.get(User, id)
    if not statement:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(statement)
    session.commit()

    return {"mensagem":"Usuário deletado com sucesso!"}
