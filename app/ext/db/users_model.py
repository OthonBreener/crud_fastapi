from typing import Optional, List
from pydantic import validator, EmailStr
from sqlmodel import Field, SQLModel
from datetime import datetime
from validate_docbr import PIS, CPF


class User(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    creation: datetime = Field(default_factory=datetime.now)
    senha: str
    senha_repet: str
    email: EmailStr
    full_name: str
    cpf: str
    pis: str


    class Config:
        orm_mode = True

    @validator('full_name', 'email', 'cpf', 'pis', 'senha', 'senha_repet')
    def nenhum_atributo_deve_ser_none(cls, valor):
        """
        Método que verifica se os dados obrigatórios não
        estão em branco.
        """

        if valor == None:
            raise ValueError(f'O campo {valor} não pode ficar em branco.')
        return valor


    @validator('full_name')
    def full_name_deve_ser_maior_que_10_caracteres(cls, name):
        """
        Método que valida o tamanho do nome completo.
        """

        if len(name) < 10:
            raise ValueError("Nome completo deve conter mais de 10 caracteres.")
        return name


    @validator('senha_repet')
    def senha_deve_ser_igual_a_senha_repet(cls, senha_repet, values):
        """
        Método que válida se as senhas são iguais.
        Input:
            senha_repet: Repetição da senha inicial
            values: Dicionário contendo os atributos da classe User
        """

        if senha_repet == values['senha']:
            return senha_repet
        raise ValueError('Senhas diferentes!')


    @validator('cpf')
    def cpf_deve_ter_digito_de_controle_valido(cls, value):
        """
        Método que valida se o cpf é válido.
        Input:
            value: CPF a ser validado
        """
        cpf = CPF()
        if cpf.validate(value) is True:
            return value

        return ValueError(f'CPF: {value}  inválido!')

    @validator('pis')
    def pis_deve_ter_digito_de_controle_valido(cls, value):
        """
        Método que valida se o pis é válido.
        Input:
            value: PIS a ser validado
        """
        pis = PIS()
        if pis.validate(value) is True:
            return value

        return ValueError(f'PIS: {value} inválido!')


class UserRead(SQLModel):
    """
    Classe utilizada para retornar apenas
    os campos selecionados para o usuário.
    """

    id: Optional[int] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    cpf: Optional[str] = None
    pis: Optional[str] = None


class UserLogin(SQLModel):

    senha: str
    email: Optional[EmailStr]
    cpf: Optional[str]
    pis: Optional[str]


class UserLoginSucess(SQLModel):
    user: UserRead
    access_token: str


class UserUpdate(SQLModel):
    """
    Classe utilizada para atualizar os dados com o método
    patch, onde todos os atributos são opcionais. Fazendo
    com que seja possível atualizar dois dados sem ter que
    reescrever todos os outros atributos a serem mantidos.
    """

    senha: Optional[str] = None
    senha_repet: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    cpf: Optional[str] = None
    pis: Optional[str] = None

    class Config:
        orm_mode = True

    @validator('full_name')
    def full_name_deve_ser_maior_que_10_caracteres(cls, name):
        """
        Método que valida o tamanho do nome completo.
        """
        if name == None:
            return name

        elif len(name) < 10:
            raise ValueError("Nome completo deve conter mais de 10 caracteres.")
        return name


    @validator('senha_repet')
    def senha_deve_ser_igual_a_senha_repet(cls, senha_repet, values):
        """
        Método que válida se as senhas são iguais.
        Input:
            senha_repet: Repetição da senha inicial
            values: Dicionário contendo os atributos da classe User
        """

        if senha_repet == values['senha']:
            return senha_repet
        raise ValueError('Senhas diferentes!')


    @validator('cpf')
    def cpf_deve_ter_digito_de_controle_valido(cls, value):
        """
        Método que valida se o cpf é válido.
        Input:
            value: CPF a ser validado
        """

        if value is None:
            return value

        cpf = CPF()
        if cpf.validate(value) is True:
            return value

        return ValueError(f'CPF: {value}  inválido!')


    @validator('pis')
    def pis_deve_ter_digito_de_controle_valido(cls, value):
        """
        Método que valida se o pis é válido.
        Input:
            value: PIS a ser validado
        """
        if value is None:
            return value

        pis = PIS()
        if pis.validate(value) is True:
            return value

        return ValueError(f'PIS: {value} inválido!')
