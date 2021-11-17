from datetime import datetime, timedelta
from jose import jwt
from app.ext.core.utils import get_env


def creation_access_token(data: dict):
    """
    Função responsável por criar um token de acesso
    do dado passado com tempo de expiração.
    """

    datas = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = 3000)
    datas.update({'exp':expire})
    token_jwt = jwt.encode(datas, get_env('SECRET_KEY'), algorithm = get_env('ALGORITHM'))
    return token_jwt


def validation_access_token(token: str):

    payload = jwt.decode(token, get_env('SECRET_KEY'), algorithms=[get_env('ALGORITHM')])
    return payload.get('sub')
