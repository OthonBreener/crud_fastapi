from sqlmodel import create_engine
from app.ext.db.users_model import User
from app.ext.db.address_model import Address
from app.ext.core.utils import get_env

#postgre_url = get_env('POSTGRE_URL')
db_url = 'postgresql://postgres:senha@localhost:5432/postgres'
engine = create_engine(db_url, echo=True)
