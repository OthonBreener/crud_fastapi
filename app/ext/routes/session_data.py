from uuid import uuid4, UUID
from fastapi import APIRouter, Response, Depends
from app.ext.core.session_backend import backend, cookie, verifier
from app.ext.db.session_data import SessionData

router = APIRouter(
    prefix="/session",
    tags = ['Session']
)

@router.get("/get_session", dependencies=[Depends(cookie)])
async def get_session(session_data: SessionData = Depends(verifier)):
    return session_data


@router.post("/create_session")
async def create_session(session_data: SessionData, response: Response):

    session = uuid4()
    await backend.create(session, session_data)
    cookie.attach_to_response(response, session)

    return f"Seção criada para {session_data.full_name}"


@router.post("/delete_session")
async def del_session(response: Response, session_id: UUID = Depends(cookie)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return "Seção deletada"
