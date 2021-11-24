from fastapi import status, Request
from typing import Dict
from httpx import Client
from validate_docbr import PIS, CPF
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from app.ext.providers.hash_provider import verification_hash
from config import TEMPLATE_FOLDER

templates = Jinja2Templates(directory=TEMPLATE_FOLDER)

def verification_type_login(username: str, password: str) -> Dict[str, str]:
    """
    Função que recebe o login do usuário e identifica
    qual o username utilizado para fazer o login.
    """

    cpf = CPF()
    if cpf.validate(username) is True:
        login = dict(cpf = username, senha = password)

    pis = PIS()
    if pis.validate(username) is True:
        login = dict(pis = username, senha = password)

    else:
        login = dict(email = username, senha = password)

    return login


def initial_page_template(request: Request, username: str, password: str,
    client: Client):
    """
    Função que recebe o login do usuario e em caso de ser
    um usuário cadastrado no sistema redireciona para a página home.
    """

    login = verification_type_login(username, password)

    result = client.post('/auth/signin', json=login, timeout=None)
    if result.status_code == 200:

        token = result.json()['access_token']
        redirect = RedirectResponse(url='/home', status_code=status.HTTP_302_FOUND)
        redirect.set_cookie('my_cookie', value=token)
        return redirect

    return templates.TemplateResponse('base.html', {"request": request})


def page_home(request: Request, client: Client):
    """
    Função que valida se o usuário pode entrar
    na página inicial.
    """

    token = request.cookies.get('my_cookie')
    if not token:
        return templates.TemplateResponse('base.html',{"request":request})

    auth_me = client.get('/auth/me', headers = {'Authorization': 'Bearer ' + token})
    if auth_me.status_code != 200:
        return templates.TemplateResponse('base.html',{"request":request})

    name = auth_me.json()[0].get('full_name')
    return templates.TemplateResponse('home.html',{"request":request, 'username': name})


def register_user_and_address(nome: str, email: str, cpf: str, pis: str,
    password: str, password2: str, country: str, state: str, city: str,
    cep: str, street: str, number: str, complement: str, client: Client):
    """
    Função que recebe os dados de cadastro do usuário
    e em caso dos dados estiverem corretos o redireciona
    para a página home.
    """
    login = dict(email = email, senha = password)

    cadastro = dict(full_name = nome,
                    email = email,
                    cpf = cpf,
                    pis = pis,
                    senha = password,
                    senha_repet = password2)

    register_datas_user = client.post("/auth/signup", json=cadastro, timeout=None)
    if register_datas_user.status_code != 200:
        return RedirectResponse('singnup', status_code=status.HTTP_302_FOUND)

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
    if register_datas_address.status_code != 200:
        return RedirectResponse('singnup', status_code=status.HTTP_302_FOUND)

    redirect = RedirectResponse(url='/home', status_code=status.HTTP_302_FOUND)
    redirect.set_cookie(key = 'my_cookie', value=token)
    return redirect


def edit_users_and_address_get(request: Request, client: Client):
    """
    Função que busca os dados de um usuário logado
    e retorna no front para alterações.
    """

    token = request.cookies.get('my_cookie')
    if not token:
        return templates.TemplateResponse('base.html',{"request":request})

    auth_me = client.get('/auth/me', headers = {'Authorization': 'Bearer ' + token})
    if auth_me.status_code != 200:
        return templates.TemplateResponse('base.html', {"request": request})

    user_id = auth_me.json()[0].get('id')

    response_user = client.get(f'/users/get/{user_id}')
    response_address = client.get(f'/address/register/get_user_id/{user_id}')
    params_user = response_user.json()[0]
    params_address = response_address.json()[0]

    if response_user.status_code == 200:

        nome = params_user.get('full_name')
        email = params_user.get('email')
        cpf = params_user.get('cpf')
        pis = params_user.get('pis')
        country = params_address.get('country')
        state = params_address.get('state')
        city = params_address.get('city')
        cep = params_address.get('cep')
        street = params_address.get('street')
        number = params_address.get('number')
        complement = params_address.get('complement')

        return templates.TemplateResponse(
            'edit_datas.html',
            {
                "request":request,
                "nome":nome, "email":email, "cpf":cpf, "pis": pis,
                "country":country, "state":state, "city":city, "cep":cep,
                "street":street, "number":number, "complement":complement
            }
        )


def edit_users_and_address_post(request: Request,
        nome: str, email: str, cpf: str, pis: str,
        password: str, password2: str, country: str, state: str, city: str,
        cep: str, street: str, number: str, complement: str, client: Client
    ):
    """
    Função que alterado os dados usuário em caso de sucesso,
    caso os dados sejam inválidos retorna para a página home.
    """

    token = request.cookies.get('my_cookie')
    response = client.get('/auth/me', headers = {'Authorization': 'Bearer ' + token})
    if response.status_code != 200:
        return RedirectResponse('/',status_code=status.HTTP_302_FOUND)

    user_id = response.json()[0].get('id')

    cadastro = dict(full_name = nome,
                    email = email,
                    cpf = cpf,
                    pis = pis,
                    senha = password,
                    senha_repet = password2)

    register_datas_user = client.patch(f"/users/patch/update/{user_id}",json=cadastro)
    if register_datas_user.status_code != 200:
        return RedirectResponse('/home', status_code=status.HTTP_302_FOUND)

    get_address_id = client.get(f"/address/register/get_user_id/{user_id}")
    id_address = get_address_id.json()[0].get('id')

    cadastro_address = dict(
        country = country,
        state = state,
        city = city,
        cep = cep,
        street = street,
        number = number,
        complement = complement)

    register_datas_address = client.patch(f'/address/register/update/{id_address}',
        json=cadastro_address, timeout=None
    )
    if register_datas_address.status_code != 200:
        return RedirectResponse('/home', status_code=status.HTTP_302_FOUND)

    return RedirectResponse(url='/edit_datas', status_code=status.HTTP_302_FOUND)


def delete_user_and_address_get(request: Request, client: Client):
    """
    Função que renderiza a página de deletar
    os dados do usuário.
    """


    token = request.cookies.get('my_cookie')
    if not token:
        return templates.TemplateResponse('base.html', {"request":request})

    auth_me = client.get('/auth/me', headers = {'Authorization': 'Bearer ' + token})
    if auth_me.status_code != 200:
        return templates.TemplateResponse('base.html', {"request":request})

    name = auth_me.json()[0].get('full_name')
    return templates.TemplateResponse('delete.html',{"request":request, "name": name})


def delete_user_and_address_post(request: Request, password: str, client: Client):
    """
    Função que deleta um usuário e apaga sua seção.
    """
    
    token = request.cookies.get('my_cookie')
    if not token:
        return templates.TemplateResponse('base.html', {"request":request})

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
