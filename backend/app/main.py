from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from enum import Enum
import bcrypt
import os

# Database
DATABASE_URL = "postgresql://mybookie_user:125701@localhost:5432/mybookie_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI App
app = FastAPI(
    title="📚 Mybookie API",
    description="""
    <div style='font-size: 16px; line-height: 1.8;'>
    
    ## 🎉 Bem-vindo à Mybookie API!
    
    Sistema completo de gerenciamento de biblioteca pessoal com autenticação segura e CRUD de livros.
    
    ### ✨ Recursos Principais
    
    - 👤 **Autenticação**: Registro e login com hash bcrypt seguro
    - 📚 **Gerenciamento de Livros**: CRUD completo com categorias
    - ⭐ **Avaliação**: Classifique livros que já leu com 5 estrelas
    - 🔍 **Filtros**: Pesquise por nome, categoria e status de leitura
    - 📖 **Status de Leitura**: Marque livros como lidos ou não lidos
    - 🔐 **Segurança**: Senhas hasheadas com bcrypt
    - 📊 **Documentação**: Swagger UI interativa
    
    ### 🛠️ Stack Tecnológico
    
    **Backend:**
    - Python 3.11+
    - FastAPI (framework moderno e rápido)
    - SQLAlchemy (ORM para banco de dados)
    - PostgreSQL (banco de dados relacional)
    - Bcrypt (hash seguro de senhas)
    - Pydantic (validação de dados)
    
    **Frontend:**
    - React 18
    - Vite (build tool)
    - Axios (cliente HTTP)
    - CSS3 (design responsivo)
    
    ### 📝 Como Usar
    
    1. Faça login ou registre uma nova conta
    2. Adicione livros com título, autor e categoria
    3. Marque como lido e deixe sua avaliação
    4. Filtre livros por nome ou status
    5. Edite ou delete livros conforme necessário
    
    ### 🔗 Endpoints Principais
    
    - `POST /api/v1/auth/register` - Criar novo usuário
    - `POST /api/v1/auth/login` - Fazer login
    - `GET /api/v1/books` - Listar todos os livros
    - `POST /api/v1/books` - Adicionar novo livro
    - `PUT /api/v1/books/{id}` - Atualizar livro
    - `DELETE /api/v1/books/{id}` - Deletar livro
    
    ### 👩‍💻 Desenvolvido por
    
    **Michele Caroline Teixeira de Oliveira**
    - Senior QA Engineer | Professora Universitária
    - 📧 michele564000@gmail.com
    - 📱 (14) 99631-2027
    - 💼 [LinkedIn](https://linkedin.com/in/michelecarolineoliveira)
    - 📍 Garça, São Paulo, Brasil
    
    ---
    
    **Versão 1.0** | Desenvolvido com ❤️ usando FastAPI e React
    
    </div>
    """,
    version="1.0.0",
    terms_of_service="https://example.com/terms",
    contact={
        "name": "Michele Caroline Teixeira de Oliveira",
        "email": "michele564000@gmail.com",
        "url": "https://linkedin.com/in/michelecarolineoliveira",
    },
    license_info={
        "name": "MIT",
    },
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= ENUMS =============
class CategoriaEnum(str, Enum):
    ficcao = "Ficção"
    romance = "Romance"
    fantasia = "Fantasia"
    tecnologia = "Tecnologia"
    historia = "História"
    educacao = "Educação"
    ciencia = "Ciência"
    infantil = "Infantil"
    poesia = "Poesia"
    biografia = "Biografia"
    autoajuda = "Autoajuda"
    negocios = "Negócios"

# ============= MODELS =============
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False, index=True)
    autor = Column(String(255), nullable=False, index=True)
    categoria = Column(String(100), nullable=True)
    lido = Column(Boolean, default=False)
    avaliacao = Column(Integer, default=0)
    status = Column(String(50), default="disponivel")
    created_at = Column(DateTime, default=datetime.utcnow)

# ============= PYDANTIC MODELS =============
class UserRegister(BaseModel):
    email: EmailStr = Field(..., description="Email único do usuário")
    username: str = Field(..., min_length=3, description="Nome de usuário")
    password: str = Field(..., min_length=6, description="Senha (mínimo 6 caracteres)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "usuario@example.com",
                "username": "usuario123",
                "password": "senha123"
            }
        }

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(..., description="Senha")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "usuario@example.com",
                "password": "senha123"
            }
        }

class BookCreate(BaseModel):
    titulo: str = Field(..., min_length=3, description="Título do livro")
    autor: str = Field(..., min_length=3, description="Autor do livro")
    categoria: CategoriaEnum = Field(..., description="Categoria/gênero do livro")
    lido: bool = Field(default=False, description="Se o livro foi lido")
    avaliacao: int = Field(default=0, ge=0, le=5, description="Avaliação de 0 a 5 estrelas")
    
    class Config:
        json_schema_extra = {
            "example": {
                "titulo": "Dom Casmurro",
                "autor": "Machado de Assis",
                "categoria": "Romance",
                "lido": True,
                "avaliacao": 5
            }
        }

class BookResponse(BaseModel):
    id: int
    titulo: str
    autor: str
    categoria: str
    lido: bool
    avaliacao: int
    status: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str

# ============= DATABASE SETUP =============
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============= HELPER FUNCTIONS =============
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def book_to_dict(book):
    return {
        "id": book.id,
        "titulo": book.titulo,
        "autor": book.autor,
        "categoria": book.categoria,
        "lido": book.lido,
        "avaliacao": book.avaliacao,
        "status": book.status
    }

# ============= ROUTES =============

@app.get("/", tags=["Sistema"], summary="Status da API")
def root():
    """Retorna o status da API Mybookie"""
    return {
        "message": "✅ Mybookie API está funcionando!",
        "version": "1.0.0",
        "status": "online"
    }

@app.get("/health", tags=["Sistema"], summary="Health Check")
def health():
    """Verifica a saúde da API"""
    return {
        "status": "✅ Healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/about", tags=["Sobre"], summary="Informações da Aplicação")
def about():
    """
    ## 📚 Sobre Mybookie
    
    Mybookie é um sistema moderno para gerenciar sua biblioteca pessoal.
    
    **Recursos:**
    - Cadastro seguro de livros
    - Avaliação com 5 estrelas
    - Filtros inteligentes
    - Interface responsiva
    """
    return {
        "name": "Mybookie",
        "version": "1.0.0",
        "description": "Sistema de gerenciamento de biblioteca pessoal",
        "author": "Michele Caroline Teixeira de Oliveira",
        "features": [
            "Autenticação com hash bcrypt",
            "CRUD completo de livros",
            "Avaliação com 5 estrelas",
            "Filtros por categoria e status",
            "API RESTful com Swagger"
        ]
    }

@app.get("/developer", tags=["Sobre"], summary="Perfil do Desenvolvedor")
def developer():
    """Retorna informações do desenvolvedor"""
    return {
        "name": "Michele Caroline Teixeira de Oliveira",
        "title": "Senior QA Engineer | Professora Universitária | Test Automation",
        "email": "michele564000@gmail.com",
        "phone": "(14) 99631-2027",
        "location": "Garça, São Paulo, Brasil",
        "linkedin": "https://linkedin.com/in/michelecarolineoliveira",
        "experience": "7+ anos em QA e Testes de Software",
        "certifications": [
            "CTFL - Certified Tester Foundation Level",
            "Selenium",
            "Capybara + Cucumber + Ruby",
            "Jasmine",
            "BDD com Cucumber"
        ]
    }

# ============= AUTHENTICATION =============

@app.post("/api/v1/auth/register", tags=["Autenticação"], status_code=201, summary="Registrar novo usuário")
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Cria um novo usuário com email e senha.
    
    **Requisitos:**
    - Email válido e único
    - Usuário único (mínimo 3 caracteres)
    - Senha com mínimo 6 caracteres
    """
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "id": new_user.id,
        "email": new_user.email,
        "username": new_user.username,
        "message": "✅ Usuário registrado com sucesso!"
    }

@app.post("/api/v1/auth/login", tags=["Autenticação"], summary="Fazer login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Faz login com email e senha.
    
    Retorna os dados do usuário se as credenciais forem corretas.
    """
    user = db.query(User).filter(User.email == user_data.email).first()
    
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "message": "✅ Login realizado com sucesso!"
    }

# ============= BOOKS CRUD =============

@app.get("/api/v1/books", tags=["Livros"], summary="Listar todos os livros")
def list_books(db: Session = Depends(get_db)):
    """
    Retorna a lista de todos os livros cadastrados.
    """
    books = db.query(Book).all()
    return [book_to_dict(book) for book in books]

@app.get("/api/v1/books/{book_id}", tags=["Livros"], summary="Obter livro por ID")
def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Retorna um livro específico pelo ID.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return book_to_dict(book)

@app.post("/api/v1/books", tags=["Livros"], status_code=201, summary="Criar novo livro")
def create_book(book_data: BookCreate, db: Session = Depends(get_db)):
    """
    Cria um novo livro com os dados fornecidos.
    
    **Campos obrigatórios:**
    - titulo
    - autor
    - categoria
    """
    db_book = Book(
        titulo=book_data.titulo,
        autor=book_data.autor,
        categoria=book_data.categoria.value,
        lido=book_data.lido,
        avaliacao=book_data.avaliacao
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    
    return {
        **book_to_dict(db_book),
        "message": "✅ Livro criado com sucesso!"
    }

@app.put("/api/v1/books/{book_id}", tags=["Livros"], summary="Atualizar livro")
def update_book(book_id: int, book_data: BookCreate, db: Session = Depends(get_db)):
    """
    Atualiza um livro existente.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    book.titulo = book_data.titulo
    book.autor = book_data.autor
    book.categoria = book_data.categoria.value
    book.lido = book_data.lido
    book.avaliacao = book_data.avaliacao
    
    db.commit()
    db.refresh(book)
    
    return {
        **book_to_dict(book),
        "message": "✅ Livro atualizado com sucesso!"
    }

@app.delete("/api/v1/books/{book_id}", tags=["Livros"], status_code=204, summary="Deletar livro")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Deleta um livro pelo ID.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    db.delete(book)
    db.commit()
    
    return {"message": "✅ Livro deletado com sucesso!"}

# ============= RUN =============
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)