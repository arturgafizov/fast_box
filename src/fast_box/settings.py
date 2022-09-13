from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 8000
    database_url: str = "postgresql+psycopg2://fast_box_user:superpassword@db/fast_box_db" #sync
    async_database_url: str = "postgresql+asyncpg://fast_box_user:superpassword@db/fast_box_db"


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)
