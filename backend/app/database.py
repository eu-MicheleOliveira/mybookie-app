from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
from app.config import get_settings

settings = get_settings()

# Engine do banco
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.SQLALCHEMY_ECHO,
    poolclass=NullPool if settings.ENVIRONMENT == "production" else None,
    connect_args={
        "connect_timeout": 10,
        "application_name": "mybookie_api"
    } if "postgresql" in settings.DATABASE_URL else {}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

def get_db() -> Session:
    """Dependency para injetar sessão do banco em rotas"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_database_connection() -> bool:
    """Verifica se banco está acessível"""
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco: {e}")
        return False

def create_all_tables():
    """Cria todas as tabelas"""
    Base.metadata.create_all(bind=engine)

def drop_all_tables():
    """Remove todas as tabelas (cuidado!!)"""
    Base.metadata.drop_all(bind=engine)

