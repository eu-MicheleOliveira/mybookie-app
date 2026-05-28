from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# ============ USER ============

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = Field(None, max_length=255)
    matricula: Optional[str] = Field(None, max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    full_name: Optional[str] = None
    matricula: Optional[str] = None

class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ============ AUTH ============

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# ============ BOOKS ============

class BookBase(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=255)
    autor: str = Field(..., min_length=3, max_length=255)
    isbn: str = Field(..., min_length=10, max_length=20)
    descricao: Optional[str] = None
    ano_publicacao: Optional[int] = None
    categoria: Optional[str] = Field(None, max_length=100)
    quantidade: int = Field(default=1, ge=1)
    status: str = Field(default="disponivel")
    imagem_url: Optional[str] = None
    editora: Optional[str] = None
    numero_paginas: Optional[int] = None
    lingua: str = Field(default="Português")

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=3)
    autor: Optional[str] = None
    descricao: Optional[str] = None
    categoria: Optional[str] = None
    quantidade: Optional[int] = None
    status: Optional[str] = None
    imagem_url: Optional[str] = None
    editora: Optional[str] = None
    numero_paginas: Optional[int] = None
    lingua: Optional[str] = None

class BookResponse(BookBase):
    id: int
    quantidade_disponivel: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ============ HEALTH CHECK ============

class HealthResponse(BaseModel):
    status: str
    environment: str
    database: bool
    version: str
    api_title: str

# ============ STATISTICS ============

class StatisticsResponse(BaseModel):
    total_livros: int
    total_usuarios: int
    livros_disponiveis: int
    livros_indisponiveis: int
    categoria_mais_populares: list

# ============ ABOUT ============

class BibliotecaInfoResponse(BaseModel):
    nome: str
    descricao: str
    admin_nome: str
    admin_email: str
    versao_api: str
    total_livros: int
    total_usuarios: int