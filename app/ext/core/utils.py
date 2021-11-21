import os
from httpx import AsyncClient


def get_env(data: str):
    """
    Função que busca uma string nas váriaveis de ambiente.
    """
    return os.environ.get(data)


async def get_async_client():
    """
    Função que retorna o cliente assíncrono do httpx.
    """
    async with AsyncClient(base_url = "http://localhost:8000") as client:
        yield client
