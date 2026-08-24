from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Названия переменных совпадают с ключами в .env (регистронезависимо)
    database_url: str
    redis_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()