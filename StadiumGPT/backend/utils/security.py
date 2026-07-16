from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    app_name: str = 'StadiumGPT API'
    environment: str = 'development'
    database_url: str = 'sqlite:///./stadiumgpt.db'
    jwt_secret_key: str = 'change-this-development-secret-before-deploying'
    jwt_algorithm: str = 'HS256'
    access_token_expire_minutes: int = 1440
    gemini_api_key: str | None = None
    gemini_model: str = 'gemini-2.0-flash'
    allowed_origins: str = 'http://localhost:3000,http://localhost:5173'
    @property
    def cors_origins(self): return [x.strip() for x in self.allowed_origins.split(',') if x.strip()]
@lru_cache
def get_settings(): return Settings()
settings = get_settings()