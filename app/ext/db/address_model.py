from typing import Optional
from pydantic import validator
from sqlmodel import Field, SQLModel
from datetime import datetime

class Address(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    creation: datetime = Field(default_factory=datetime.now)
    country: str
    state: str
    CEP: str
    city: str
    street: str
    number: int
    complement: Optional[str]
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

    class Config:
        orm_mode = True

    @validator('country', 'state', 'CEP', 'city', 'street', 'number')
    def nenhum_atributo_deve_ser_none(cls, value):
        """
        Método que valida se os dados obrigatórios
        não estão em branco.
        """

        if value is None:
            raise ValueError(f'O campo {value} não pode ficar em branco.')
        return value

    @validator('state', 'city', 'street', 'country')
    def estado_deve_ser_maior_que_dois_caracteres(cls, value):

        if len(value) < 2:
            raise ValueError(f'O campo {value} deve ser maior que dois caracteres')
        return value


class AddressRead(SQLModel):

    country: str
    state: str
    CEP: str
    city: str
    street: str
    number: int
    complement: str
    user_id: Optional[int]

    class Config:
        orm_mode: True


class AddressUpdate(SQLModel):
    """
    Classe utilizada para atualizar os dados com o método
    patch, onde todos os atributos são opcionais. Fazendo
    com que seja possível atualizar dois dados sem ter que
    reescrever todos os outros atributos a serem mantidos.
    """

    country: Optional[str]
    state: Optional[str]
    CEP: Optional[str]
    city: Optional[str]
    street: Optional[str]
    number: Optional[int]
    complement: Optional[str]

    class Config:
        orm_mode = True

    @validator('state', 'city', 'street', 'country')
    def estado_deve_ser_maior_que_dois_caracteres(cls, value):

        if value is None:
            return value

        elif len(value) < 2:
            raise ValueError(f'O campo {value} deve ser maior que dois caracteres')
        return value
