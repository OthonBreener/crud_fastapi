from datetime import datetime, timedelta
from jose import jwt
from app.ext.core.config import settings


def creation_access_token(data: dict):
    """
    Função responsável por criar um token de acesso
    do dado passado com tempo de expiração.
    """

    datas = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = 3000)
    datas.update({'exp':expire})
    token_jwt = jwt.encode(datas, settings.secret_key, algorithm = settings.algorithm)
    return token_jwt


def validation_access_token(token: str):

    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    return payload.get('sub')
