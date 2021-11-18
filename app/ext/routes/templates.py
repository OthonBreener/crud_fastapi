from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


router = APIRouter(
    responses={404: {"description": "Not Found"}},
)

templates = Jinja2Templates(directory='templates')

@router.get("/", response_class=HTMLResponse)
async def initial_page_get(request: Request):
    return templates.TemplateResponse('base.html', {"request":request})


@router.post("/", response_class=HTMLResponse)
async def initial_page_post(request: Request, user: str = Form(...), password: str = Form(...)):
    print(user)
    print(password)
    return templates.TemplateResponse('base.html', {"request":request})




@router.get("/singup", response_class=HTMLResponse)
async def singup(request: Request):
    return templates.TemplateResponse('singup.html', {"request":request})
