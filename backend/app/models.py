from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from datetime import datetime
from app.database import Base

class User(Base):
    """Modelo de usuário (Leitora)"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    matricula = Column(String(50), nullable=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="user", nullable=False)  # "user" ou "admin"
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), 
                       onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"

class Book(Base):
    """Modelo de livro/produto"""
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False, index=True)
    autor = Column(String(255), nullable=False, index=True)
    isbn = Column(String(20), unique=True, nullable=False, index=True)
    descricao = Column(Text, nullable=True)
    ano_publicacao = Column(Integer, nullable=True)
    categoria = Column(String(100), nullable=True, index=True)
    quantidade = Column(Integer, default=1, nullable=False)
    quantidade_disponivel = Column(Integer, default=1, nullable=False)
    status = Column(String(50), default="disponivel", nullable=False, index=True)
    imagem_url = Column(String(500), nullable=True)
    editora = Column(String(255), nullable=True)
    numero_paginas = Column(Integer, nullable=True)
    lingua = Column(String(50), default="Português", nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), 
                       onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Book(id={self.id}, titulo={self.titulo}, autor={self.autor})>"

