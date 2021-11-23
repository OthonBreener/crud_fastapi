import redis, json
from httpx import Client
from fastapi import APIRouter, Request, Form, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from validate_docbr import PIS, CPF
from app.ext.core.utils import get_client
from config import TEMPLATE_FOLDER

router = APIRouter(
    tags=['Tempates'],
    responses={404: {"description": "Not Found"}},
)

templates = Jinja2Templates(directory=TEMPLATE_FOLDER)

redis_client = redis.Redis(host='localhost', port='6379', db=0)

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
        token = result.json()['access_token']
        redis_client.set('token', token)

        return RedirectResponse(url='/home', status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse('base.html', {"request":request})

####################### Page Home #########################################
@router.get("/home", response_class=HTMLResponse)
def home(request: Request, client: Client = Depends(get_client)):

    token = redis_client.get('token')
    bearer = token.decode('utf-8')

    response = client.get('/auth/me', headers = {'Authorization': 'Bearer ' + bearer})
    data = response.json()
    name = data[0].get('full_name')

    return templates.TemplateResponse('home.html',
            {"request":request, 'username': name})

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
    bearer = logar_usuario.json().get('access_token')

    auth_me = client.get('/auth/me', headers={'Authorization': 'Bearer ' + bearer}, timeout=None)

    user_id = auth_me.json()[0].get('id')
    user_name = auth_me.json()[0].get('full_name')
    redis_client.set("user_name", user_name)

    cadastro_address = dict(
        country = country,
        state = state,
        city = city,
        cep = cep,
        street = street,
        number = number,
        complement = complement,
        user_id = user_id)

    register_datas_address = client.post('/address/register', json=cadastro_address, timeout=None)

    return RedirectResponse(url='/home', status_code=status.HTTP_302_FOUND)

#################### Pagina de edição de dados do usuário ###################
@router.get("/edit_datas", response_class=HTMLResponse)
def edit_user(request: Request, client: Client = Depends(get_client)):

    token = redis_client.get('token')
    bearer = token.decode('utf-8')
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

    token = redis_client.get('token')
    bearer = token.decode('utf-8')
    auth_me = client.get('/auth/me', headers={'Authorization': 'Bearer ' + bearer}, timeout=None)
    user_id = auth_me.json()[0].get('id')

    import ipdb; ipdb.set_trace()

    cadastro = dict(full_name = nome,
                    email = email,
                    cpf = cpf,
                    pis = pis)

    register_datas_user = client.patch(
        f"/auth/patch/update/{user_id}",
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
