from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    salt: str
    db_dsn: str
    db_dsn_test: str

    class Config:
        env_file = ".env"


settings = Settings()