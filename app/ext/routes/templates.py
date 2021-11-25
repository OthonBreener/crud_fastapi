from httpx import Client
from fastapi import APIRouter, Request, Form, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.ext.core.utils import get_client
from app.ext.controllers.templates_controller import (
    register_user_and_address,
    delete_user_and_address_post,
    delete_user_and_address_get,
    edit_users_and_address_post,
    edit_users_and_address_get,
    initial_page_template,
    page_home
)
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

    return initial_page_template(request, username, password, client)

####################### Page Home #########################################

@router.get("/home", response_class=HTMLResponse)
def home(request: Request, client: Client = Depends(get_client)):

    return page_home(request, client)

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

    return edit_users_and_address_get(request, client)


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

    return edit_users_and_address_post(
        request, nome, email, cpf, pis, password,
        password2, country, state, city, cep, street,
        number, complement, client
        )

######################## Pagina para deletar dados do usuario ######################

@router.get('/delete', response_class=HTMLResponse)
def delete_user(request: Request, client: Client = Depends(get_client)):

    return delete_user_and_address_get(request, client)


@router.post('/delete', response_class=RedirectResponse, status_code=302)
def delete_user(request: Request,
    password: str = Form(...),
    client: Client = Depends(get_client)):

    return delete_user_and_address_post(request, password, client)
