import redis, json
from httpx import AsyncClient
from fastapi import APIRouter, Request, Form, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from validate_docbr import PIS, CPF
from app.ext.core.utils import get_async_client

router = APIRouter(
    tags=['Tempates'],
    responses={404: {"description": "Not Found"}},
)

templates = Jinja2Templates(directory='templates')

redis_client = redis.Redis(host='localhost', port='6379', db=0)
##################### Login ##########################
@router.get("/", response_class=HTMLResponse)
async def initial_page_get(request: Request):
    return templates.TemplateResponse('base.html', {"request":request})


@router.post("/", response_class=HTMLResponse)
async def initial_page_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    client: AsyncClient = Depends(get_async_client)):

    cpf = CPF()
    if cpf.validate(username) is True:
        login = dict(CPF = username, senha = password)

    pis = PIS()
    if pis.validate(username) is True:
        login = dict(PIS = username, senha = password)

    else:
        login = dict(email = username, senha = password)


    result = await client.post('/auth/signin', json=login, timeout=None)

    return RedirectResponse(url='/home', status_code=status.HTTP_302_FOUND)

##################### Cadastro  usuário ########################

@router.get("/singnup", response_class=HTMLResponse)
async def teste_cadastro(request: Request):

    return templates.TemplateResponse('singnup.html', {"request": request})


@router.post("/singnup", response_class=RedirectResponse, status_code=302)
async def teste_cadastro(
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
    client: AsyncClient = Depends(get_async_client)):

    login = dict(email = email, senha = password)

    cadastro = dict(full_name = nome,
                    email = email,
                    CPF = cpf,
                    PIS = pis,
                    senha = password,
                    senha_repet = password2)


    register_datas_user = await client.post("/auth/signup", json=cadastro, timeout=None)

    logar_usuario = await client.post('/auth/signin', json=login, timeout=None)
    bearer = logar_usuario.json().get('access_token')

    auth_me = await client.get('/auth/me', headers={'Authorization': 'Bearer ' + bearer}, timeout=None)

    user_id = auth_me.json()[0].get('id')
    user_name = auth_me.json()[0].get('full_name')
    redis_client.set("user_name", user_name)

    cadastro_address = dict(
        country = country,
        state = state,
        city = city,
        CEP = cep,
        street = street,
        number = number,
        complement = complement,
        user_id = user_id)

    register_datas_address = await client.post('/address/register', json=cadastro_address, timeout=None)

    return RedirectResponse(url='/home', status_code=status.HTTP_302_FOUND)


####################### Page Home #########################################
@router.get("/home", response_class=HTMLResponse)
async def home(request: Request):

    user = json.loads(redis_client.get('user_name'))
    return templates.TemplateResponse('home.html',
            {"request":request, 'username': user})


#################### Pagina de edição de dados do usuário ###################
@router.get("/user_datas", response_class=HTMLResponse)
async def edit_user(request: Request):

    params = []

    title = 'Dados do Usuário'
    nome = ''
    email = ''
    cpf = ''
    pis = ''
    password = ''
    password2 = ''
    country = ''
    state = ''
    city = ''
    cep = ''
    street = ''
    number = ''
    complement = ''

    if params:
        nome = params.get('name')
        email = params.get('email')
        cpf = params.get('cpf')
        pis = params.get('pis')
        password = params.get('password')
        password2 = params.get('password2')
        country = address.get('country')
        state = address.get('state')
        city = address.get('city')
        cep = address.get('CEP')
        street = address.get('street')
        number = address.get('number')
        complement = address.get('complement')

    return templates.TemplateResponse(
        'edit_user.html',
        {
            "request":request,
            "nome":nome, "email":email, "cpf":cpf, "pis": pis,
            "password": password, "password2": password2, "title": title,
            "request":request, "country":country, "state":state, "city":city,
            "cep":cep, "street":street, "number":number, "complement":complement
        }
    )
