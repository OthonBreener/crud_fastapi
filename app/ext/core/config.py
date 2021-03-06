from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str

    class Config:
        env_file = '.env'

settings = Settings()
