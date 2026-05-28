import os
from functools import lru_cache
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_TITLE: str = "Mybookie"
    API_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    DATABASE_URL: str = "postgresql://mybookie_user:senha_segura_123@localhost:5432/mybookie_db"
    SQLALCHEMY_ECHO: bool = False
    SECRET_KEY: str = "sua-chave-super-secreta-nao-compartilhe-em-producao-mude-isso"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]
    BIBLIOTECA_NOME: str = "Mybookie"
    BIBLIOTECA_ADMIN_EMAIL: str = "admin@mybookie.com"
    BIBLIOTECA_ADMIN_NOME: str = "Administrador"
    BIBLIOTECA_DESCRICAO: str = "Sistema de gerenciamento de biblioteca para aulas"
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

