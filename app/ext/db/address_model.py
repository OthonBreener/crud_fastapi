from typing import Optional
from pydantic import validator
from sqlmodel import Field, SQLModel
from datetime import datetime
from pycep_correios import get_address_from_cep, WebService, exceptions


class Address(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    creation: datetime = Field(default_factory=datetime.now)
    country: str
    state: str
    cep: str
    city: str
    street: str
    number: str
    complement: str
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

    class Config:
        orm_mode = True


    @validator('country', 'state', 'cep', 'city', 'street', 'number')
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
        """
        Método que valida o tamanho mínimo dos dados inseridos.
        """

        if len(value) < 2:
            raise ValueError(f'O campo {value} deve ser maior que dois caracteres')
        return value


    #@validator('cep')
    def cep_deve_ser_valido(cls, value):
        """
        Método que valida se o cep inserido é válido.
        """

        try:
            address = get_address_from_cep(value, webservice=WebService.APICEP)
            return address.get('cep')

        except exceptions.InvalidCEP as eic:
            return eic

        except exceptions.CEPNotFound as ecnf:
            return ecnf


class AddressRead(SQLModel):

    country: Optional[str] = None
    state: Optional[str] = None
    cep: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    number: Optional[str] = None
    complement: Optional[str] = None
    user_id: Optional[int] = None



class AddressUpdate(SQLModel):
    """
    Classe utilizada para atualizar os dados com o método
    patch, onde todos os atributos são opcionais. Fazendo
    com que seja possível atualizar dois dados sem ter que
    reescrever todos os outros atributos a serem mantidos.
    """

    country: Optional[str]
    state: Optional[str]
    cep: Optional[str]
    city: Optional[str]
    street: Optional[str]
    number: Optional[str]
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
