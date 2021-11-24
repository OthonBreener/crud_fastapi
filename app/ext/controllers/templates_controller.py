from fastapi import status, Request
from typing import Dict
from httpx import Client
from validate_docbr import PIS, CPF
from fastapi.responses import RedirectResponse, HTMLResponse
from app.ext.providers.hash_provider import verification_hash

def verification_type_login(username: str, password: str) -> Dict[str, str]:

    cpf = CPF()
    if cpf.validate(username) is True:
        login = dict(cpf = username, senha = password)

    pis = PIS()
    if pis.validate(username) is True:
        login = dict(pis = username, senha = password)

    else:
        login = dict(email = username, senha = password)

    return login


def register_user_and_address(nome: str, email: str, cpf: str, pis: str,
    password: str, password2: str, country: str, state: str, city: str,
    cep: str, street: str, number: str, complement: str, client: Client):

    login = dict(email = email, senha = password)

    cadastro = dict(full_name = nome,
                    email = email,
                    cpf = cpf,
                    pis = pis,
                    senha = password,
                    senha_repet = password2)

    register_datas_user = client.post("/auth/signup", json=cadastro, timeout=None)

    logar_usuario = client.post('/auth/signin', json=login, timeout=None)
    token = logar_usuario.json()['access_token']
    user_id = register_datas_user.json()['id']

    cadastro_address = dict(
        country = country,
        state = state,
        city = city,
        cep = cep,
        street = street,
        number = number,
        complement = complement,
        user_id = user_id)

    register_datas_address = client.post('/address/register', json=cadastro_address)

    redirect = RedirectResponse(url='/home', status_code=status.HTTP_302_FOUND)
    redirect.set_cookie(key = 'my_cookie', value=token)

    return redirect


def delete_user_and_address(request: Request, password: str, client: Client, token: str,
    templates):

    response = client.get('/auth/me', headers = {'Authorization': 'Bearer ' + token})
    email = response.json()[0].get('email')
    user_id = response.json()[0].get('id')

    response_pass = client.get(f'/users/get_pass/{email}')
    senha_hash = response_pass.json()[0].get('senha')

    if verification_hash(password, senha_hash) is True:

        address = client.get(f'/address/register/get_user_id/{user_id}')
        address_id = address.json()[0].get('id')

        delete_address = client.delete(f'/address/register/delete/{address_id}')
        delete_user = client.delete(f'/users/delete/{user_id}')

        if delete_user.status_code == 200:
            redirect = RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)
            redirect.delete_cookie('my_cookie')
            return redirect

        return templates.TemplateResponse('base.html', {"request":request})

    return templates.TemplateResponse('delete.html', {"request":request})
