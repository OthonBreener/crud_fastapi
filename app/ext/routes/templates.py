import redis, json
from httpx import Client
from fastapi import APIRouter, Request, Form, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.ext.core.utils import get_client
from app.ext.controllers.templates_controller import (
    verification_type_login,
    register_user_and_address,
    delete_user_and_address
)

from config import TEMPLATE_FOLDER

router = APIRouter(
    tags=['Tempates'],
    responses={404: {"description": "Not Found"}},
)

templates = Jinja2Templates(directory=TEMPLATE_FOLDER)
client_redis = redis.Redis(host='localhost', port=6379, db=0)

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

    login = verification_type_login(username, password)

    result = client.post('/auth/signin', json=login, timeout=None)
    if result.status_code == 200:

        token = result.json()['access_token']
        redirect = RedirectResponse(url='/home', status_code=status.HTTP_302_FOUND)
        redirect.set_cookie('my_cookie', value=token)
        return redirect

    return templates.TemplateResponse(
        'base.html',
        {"request": request})

####################### Page Home #########################################

@router.get("/home", response_class=HTMLResponse)
def home(request: Request, client: Client = Depends(get_client)):

    token = request.cookies.get('my_cookie')
    if not token:
        return templates.TemplateResponse('base.html',{"request":request})

    auth_me = client.get('/auth/me', headers = {'Authorization': 'Bearer ' + token})
    if auth_me.status_code != 200:
        return templates.TemplateResponse('base.html',{"request":request})

    name = auth_me.json()[0].get('full_name')

    return templates.TemplateResponse('home.html',
            {"request":request, 'username': name})

##################### Rota para deslogar ############################

@router.get("/logout", response_class=RedirectResponse, status_code=302)
def logout(request: Request):

    redirect = RedirectResponse('/', status_code=status.HTTP_302_FOUND)
    redirect.delete_cookie('my_cookie')
    return redirect

##################### Cadastro  usuário #############################

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

    return register_user_and_address(
        nome, email, cpf, pis, password, password2,
        country, state, city, cep, street, number,
        complement, client
        )

#################### Pagina de edição de dados do usuário ###################

@router.get("/edit_datas", response_class=HTMLResponse)
def edit_user(request: Request, client: Client = Depends(get_client)):

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

    token = request.cookies.get('my_cookie')
    response = client.get('/auth/me', headers = {'Authorization': 'Bearer ' + token})
    user_id = response.json()[0].get('id')

    cadastro = dict(full_name = nome,
                    email = email,
                    cpf = cpf,
                    pis = pis,
                    senha = password,
                    senha_repet = password2)

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

    token = request.cookies.get('my_cookie')
    if not token:
        return templates.TemplateResponse('base.html', {"request":request})

    auth_me = client.get('/auth/me', headers = {'Authorization': 'Bearer ' + token})
    if auth_me.status_code != 200:
        return templates.TemplateResponse('base.html', {"request":request})

    name = auth_me.json()[0].get('full_name')
    return templates.TemplateResponse('delete.html',
        {"request":request, "name": name})


@router.post('/delete', response_class=RedirectResponse, status_code=302)
def delete_user(request: Request,
    password: str = Form(...),
    client: Client = Depends(get_client)):

    token = request.cookies.get('my_cookie')
    if not token:
        return templates.TemplateResponse('base.html', {"request":request})

    return delete_user_and_address(request, password, client, token, templates)
