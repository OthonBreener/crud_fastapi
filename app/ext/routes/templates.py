import redis, json
from httpx import Client
from fastapi import APIRouter, Request, Form, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from validate_docbr import PIS, CPF
from app.ext.core.utils import get_client
from app.ext.providers.hash_provider import verification_hash
from config import TEMPLATE_FOLDER

router = APIRouter(
    tags=['Tempates'],
    responses={404: {"description": "Not Found"}},
)

templates = Jinja2Templates(directory=TEMPLATE_FOLDER)

##################### Login ##########################

@router.get("/", response_class=HTMLResponse)
def initial_page_get(request: Request):
    return templates.TemplateResponse('base.html', {"request":request})


@router.post("/", response_class=HTMLResponse)
def initial_page(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    client: Client = Depends(get_client)):

    cpf = CPF()
    if cpf.validate(username) is True:
        login = dict(cpf = username, senha = password)

    pis = PIS()
    if pis.validate(username) is True:
        login = dict(pis = username, senha = password)

    else:
        login = dict(email = username, senha = password)

    result = client.post('/auth/signin', json=login, timeout=None)
    if result.status_code == 200:

        email = result.json()['user'].get('email')
        token = result.json()['access_token']
        response = client.get('/auth/me', headers = {'Authorization': 'Bearer ' + token})
        name = response.json()[0].get('full_name')

        session_data = dict(full_name = name, token = token, email = email)
        response_session = client.post('/session/create_session', json = session_data)

        return RedirectResponse(url='/home', status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse(
        'base.html',
        {"request": request,
        "menssage": "Senha incorreta!"})

####################### Page Home #########################################
@router.get("/home", response_class=HTMLResponse)
def home(request: Request, client: Client = Depends(get_client)):

    response = client.get('/session/get_session')
    name = response.json()[0].get('full_name')

    return templates.TemplateResponse('home.html',
            {"request":request, 'username': name, 'message': ''})

##################### Cadastro  usuário ########################

@router.get("/singnup", response_class=HTMLResponse)
def singnup(request: Request):

    return templates.TemplateResponse('singnup.html', {"request": request})


@router.post("/singnup", response_class=RedirectResponse, status_code=302)
def singnup(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    cpf: str = Form(...),
    pis: str = Form(...),
    password: str = Form(...),
    password2: str = Form(...),
    country: str = Form(...),
    state: str = Form(...),
    city: str = Form(...),
    cep: str = Form(...),
    street: str = Form(...),
    number: str = Form(...),
    complement: str = Form(...),
    client: Client = Depends(get_client)):

    login = dict(email = email, senha = password)

    cadastro = dict(full_name = nome,
                    email = email,
                    cpf = cpf,
                    pis = pis,
                    senha = password,
                    senha_repet = password2)

    register_datas_user = client.post("/auth/signup", json=cadastro, timeout=None)

    logar_usuario = client.post('/auth/signin', json=login, timeout=None)

    email = logar_usuario.json()['user'].get('email')
    token = logar_usuario.json()['access_token']
    auth_me = client.get('/auth/me', headers = {'Authorization': 'Bearer ' + token})
    name = response.json()[0].get('full_name')
    session_data = dict(full_name = name, token = token, email = email)
    response_session = client.post('/session/create_session', json = session_data)
    user_id = auth_me.json()[0].get('id')

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

    return RedirectResponse(url='/home', status_code=status.HTTP_302_FOUND)

#################### Pagina de edição de dados do usuário ###################
@router.get("/edit_datas", response_class=HTMLResponse)
def edit_user(request: Request, client: Client = Depends(get_client)):


    response_session = client.get('/session/get_session')
    bearer = response_session.get('token')
    response = client.get('/auth/me', headers = {'Authorization': 'Bearer ' + bearer})
    data = response.json()
    user_id = data[0].get('id')

    response_user = client.get(f'/users/get/{user_id}')
    response_address = client.get(f'/address/register/get_user_id/{user_id}')

    params_user = response_user.json()[0]
    params_address = response_address.json()[0]

    if response_user.status_code == 200:

        nome = params_user.get('full_name')
        email = params_user.get('email')
        cpf = params_user.get('cpf')
        pis = params_user.get('pis')
        password = params_user.get('password')
        password2 = params_user.get('password2')
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
                "password": password, "password2": password2, "country":country,
                "state":state, "city":city, "cep":cep, "street":street, "number":number,
                "complement":complement
            }
        )


@router.post("/edit_datas", response_class=RedirectResponse, status_code=302)
def singnup(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    cpf: str = Form(...),
    pis: str = Form(...),
    password: str = Form(...),
    password2: str = Form(...),
    country: str = Form(...),
    state: str = Form(...),
    city: str = Form(...),
    cep: str = Form(...),
    street: str = Form(...),
    number: str = Form(...),
    complement: str = Form(...),
    client: Client = Depends(get_client)):

    response_session = client.get('/session/get_session')
    bearer = response_session.get('token')
    auth_me = client.get('/auth/me', headers={'Authorization': 'Bearer ' + bearer})
    user_id = auth_me.json()[0].get('id')

    cadastro = dict(full_name = nome,
                    email = email,
                    cpf = cpf,
                    pis = pis)

    register_datas_user = client.patch(f"/users/patch/update/{user_id}",
        json=cadastro)

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
        json=cadastro_address)

    return RedirectResponse(url='/home', status_code=status.HTTP_302_FOUND)


######################## Pagina para deletar dados do usuario ######################

@router.get('/delete', response_class=HTMLResponse)
def delete_user(request: Request, client: Client = Depends(get_client)):

    response_session = client.get('/session/get_session')
    bearer = response_session.get('token')
    name = response_session.get('full_name')

    return templates.TemplateResponse('delete.html',
        {"request":request, "name": name})


@router.post('/delete', response_class=RedirectResponse, status_code=302)
def delete_user(request: Request,
    password: str = Form(...),
    client: Client = Depends(get_client)):

    response_session = client.get('/session/get_session')
    bearer = response_session.get('token')
    email = response_session.get('email')

    response_pass = client.get(f'/users/get_pass/{email}')
    senha_hash = response_pass.json()[0].get('senha')

    if verification_hash(password, senha_hash) is True:

        # deleta a seção do usuário e o usuário do banco de dados
        response_delete_session = client.delete('/session/delete_session')
        session_delte = client.delete(f'/users/delete/{user_id}')
        if session_delte.status_code == 200:
            return templates.TemplateResponse('base.html', {"request":request})

        return templates.TemplateResponse('edit_datas.html', {"request":request})

    return templates.TemplateResponse('edit_datas.html', {"request":request})
