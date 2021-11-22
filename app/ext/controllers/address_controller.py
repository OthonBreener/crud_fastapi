from typing import List
from fastapi import HTTPException, Depends
from sqlmodel import Session, select
from app.ext.db.address_model import Address, AddressUpdate

def add_address(address: Address, session: Session) -> Address:
    """
    Método que adiciona o endereço do usuário.
    Input:
        address: Endereço
    """

    session.add(address)
    session.commit()
    session.refresh(address)


def find_address(session: Session) -> List[Address]:
    """
    Função que busca todos os endereços
    cadastrados no banco de dados.
    """

    statement = select(Address)
    result = session.exec(statement)
    results = result.all()

    return results


def find_address_by_id(id: int, session: Session) -> List[Address]:
    """
    Função que busca um endereço através de
    seu id no banco de dados. O método scalars()
    foi utilizado para retornar apenas um json com os atributos
    sem o nome da classe.
    Input:
        id: Id de um endereço no banco de dados
    """

    statement = select(Address).where(Address.id == id)
    result = session.execute(statement)
    results = result.scalars().all()
    if not results:
        raise HTTPException(status_code=404, detail='Address not found!')

    return results


def find_address_by_id_user(user_id: int, session: Session) -> List[Address]:
    """
    Função que busca um endereço no banco de dados
    através do id do usuário.
    Input:
        user_id: Id do usuário relacionado com o endereço.
    """

    statement = select(Address).where(Address.user_id == user_id)
    result = session.execute(statement)
    results = result.scalars().all()
    if not results:
        raise HTTPException(status_code=404, detail='Address not found!')

    return results


def update_address(id: int, address: AddressUpdate, session: Session) -> AddressUpdate:
    """
    Método que atualiza um endereço no banco de dados,
    o parâmetro 'exclude_unset=True' faz com que apenas
    os valores enviados pelo cliente sejam incluidos.
    Input:
        id: Id de um endereço a ser atualizado.
        address: Request com os dados a serem atualizados
    """

    db_address = session.get(Address, id)
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")

    address_data = address.dict(exclude_unset=True)
    for key, value in address_data.items():
        setattr(db_address, key, value)

    session.add(db_address)
    session.commit()
    session.refresh(db_address)

    return db_address


def remove_address(id: int, session: Session) -> str:
    """
    Função que deleta um endereço do banco dados.
    """

    statement = select(Address).where(Address.id == id)
    result = session.exec(statement)
    address = result.one()
    session.delete(address)
    session.commit()

    return "Endereço deletado com sucesso!"
