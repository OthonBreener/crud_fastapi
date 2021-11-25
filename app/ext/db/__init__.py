from sqlmodel import create_engine
from app.ext.db.users_model import User
from app.ext.db.address_model import Address
from app.ext.core.config import settings

engine = create_engine(settings.database_url, echo=True)
