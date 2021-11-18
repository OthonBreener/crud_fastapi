from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse


router = APIRouter(
    responses={404: {"description": "Not Found"}},
)

templates = Jinja2Templates(directory='templates')

########## Login ############
@router.get("/", response_class=HTMLResponse)
async def initial_page_get(request: Request):
    return templates.TemplateResponse('base.html', {"request":request})


@router.post("/", response_class=HTMLResponse)
async def initial_page_post(request: Request, username: str = Form(...), password: str = Form(...)):
    print(username)
    print(password)
    return templates.TemplateResponse('base.html', {"request":request})


######## Cadastro  usuário ###########
@router.get("/singup", response_class=HTMLResponse)
async def singup(request: Request):
    return templates.TemplateResponse('singup.html', {"request":request})

@router.post("/singup", response_class=RedirectResponse, status_code=302)
async def singup_address(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    cpf: str = Form(...),
    pis: str = Form(...),
    password: str = Form(...),
    password2: str = Form(...)):

    cadastro = dict(full_name = nome,
                    email = email,
                    CPF = cpf,
                    PIS = pis,
                    senha = password,
                    senha_repet = password2)

    print(cadastro)

    return "http://localhost:8000/"


######## Cadastro  endereço ###########
@router.get("/singup_address", response_class=HTMLResponse)
async def singup_address(request: Request):
    return templates.TemplateResponse('singup_address.html', {"request":request})

@router.post("/singup_address", response_class=RedirectResponse, status_code=302)
async def singup_address(
    request: Request,
    country: str = Form(...),
    state: str = Form(...),
    city: str = Form(...),
    cep: str = Form(...),
    street: str = Form(...),
    number: str = Form(...),
    complement: str = Form(...)):

    cadastro_address = dict(country = country,
                    state = state,
                    city = city,
                    cep = cep,
                    street = street,
                    number = number,
                    complement = complement)

    print(cadastro)

    return "http://localhost:8000/"
