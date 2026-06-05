from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String, DateTime, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from pydantic import BaseModel, EmailStr
import bcrypt

# ===== BANCO DE DADOS =====
DATABASE_URL = "postgresql://mybookie_user:125701@localhost:5432/mybookie_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ===== MODELOS =====
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False, index=True)
    autor = Column(String(255), nullable=False, index=True)
    isbn = Column(String(20), unique=True, nullable=False)
    descricao = Column(Text, nullable=True)
    categoria = Column(String(100), nullable=True)
    quantidade = Column(Integer, default=1)
    status = Column(String(50), default="disponivel")
    created_at = Column(DateTime, default=datetime.utcnow)

# Criar tabelas
Base.metadata.create_all(bind=engine)

# ===== SCHEMAS =====
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class BookCreate(BaseModel):
    titulo: str
    autor: str
    isbn: str
    descricao: str = None
    categoria: str = None
    quantidade: int = 1

# ===== FUNÇÕES UTILITÁRIAS =====
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def book_to_dict(book):
    """Converte objeto Book para dicionário"""
    return {
        "id": book.id,
        "titulo": book.titulo,
        "autor": book.autor,
        "isbn": book.isbn,
        "descricao": book.descricao,
        "categoria": book.categoria,
        "quantidade": book.quantidade,
        "status": book.status
    }

# ===== FASTAPI APP =====
app = FastAPI(
    title="Mybookie",
    version="1.0.0",
    description="API de Biblioteca para Aulas"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== ROTAS SISTEMA =====

@app.get("/")
async def root():
    return {
        "message": "Bem-vindo ao Mybookie",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/about")
async def about():
    return {
        "nome": "Mybookie",
        "descricao": "Sistema de gerenciamento de biblioteca para aulas",
        "admin_nome": "Administrador",
        "admin_email": "admin@mybookie.com",
        "versao_api": "1.0.0",
        "total_livros": 0,
        "total_usuarios": 0
    }

# ===== AUTH ROUTES =====

@app.post("/api/v1/auth/register", status_code=201)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Registra um novo usuário"""
    
    # Verifica se email já existe
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado"
        )
    
    # Verifica se username já existe
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username já existe"
        )
    
    # Cria novo usuário
    db_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hash_password(user_data.password)
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {
        "id": db_user.id,
        "email": db_user.email,
        "username": db_user.username,
        "message": "Usuário criado com sucesso!"
    }

@app.post("/api/v1/auth/login")
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Faz login e retorna dados do usuário"""
    
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "message": "Login bem-sucedido"
    }

# ===== BOOKS ROUTES =====

@app.get("/api/v1/books")
async def list_books(db: Session = Depends(get_db)):
    """Lista todos os livros"""
    books = db.query(Book).all()
    return [book_to_dict(book) for book in books]

@app.get("/api/v1/books/{book_id}")
async def get_book(book_id: int, db: Session = Depends(get_db)):
    """Obtém um livro específico"""
    book = db.query(Book).filter(Book.id == book_id).first()
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado"
        )
    
    return book_to_dict(book)

@app.post("/api/v1/books", status_code=201)
async def create_book(book_data: BookCreate, db: Session = Depends(get_db)):
    """Cria um novo livro (admin)"""
    
    # Verifica se ISBN já existe
    existing_book = db.query(Book).filter(Book.isbn == book_data.isbn).first()
    if existing_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ISBN já existe"
        )
    
    db_book = Book(**book_data.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    
    return book_to_dict(db_book)

@app.put("/api/v1/books/{book_id}")
async def update_book(book_id: int, book_data: BookCreate, db: Session = Depends(get_db)):
    """Atualiza um livro (admin)"""
    
    db_book = db.query(Book).filter(Book.id == book_id).first()
    
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado"
        )
    
    update_data = book_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_book, field, value)
    
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    
    return book_to_dict(db_book)

@app.delete("/api/v1/books/{book_id}", status_code=204)
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Deleta um livro (admin)"""
    
    db_book = db.query(Book).filter(Book.id == book_id).first()
    
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado"
        )
    
    db.delete(db_book)
    db.commit()
    
    return None