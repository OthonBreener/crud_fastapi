from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.ext.db.users_model import User
from app.ext.db.address_model import Address
from app.ext.core.utils import get_env

#postgre_url = get_env('POSTGRE_URL')
postgre_url = 'postgresql://postgres:senha@localhost:5432/postgres'
engine = create_async_engine(postgre_url, echo=True, future=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_= AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
