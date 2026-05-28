from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app.models import User, Book
from app.schemas import BookCreate, BookUpdate, BookResponse
from app.auth import get_current_user, get_current_admin
from typing import List

router = APIRouter(prefix="/books", tags=["Livros"])

@router.post(
    "/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo livro",
    description="Apenas administradores podem criar livros"
)
async def create_book(
    book_data: BookCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Cria um novo livro na biblioteca.
    
    **Campos obrigatórios:**
    - titulo
    - autor
    - isbn
    - quantidade
    """
    
    # Verifica se ISBN já existe
    existing_book = db.query(Book).filter(Book.isbn == book_data.isbn).first()
    if existing_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ISBN já existe no banco"
        )
    
    db_book = Book(**book_data.dict())
    db_book.quantidade_disponivel = book_data.quantidade
    
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.get(
    "/",
    response_model=List[BookResponse],
    summary="Listar todos os livros",
    description="Retorna lista paginada de livros"
)
async def list_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    categoria: str = Query(None),
    status_filter: str = Query(None),
    search: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lista todos os livros com filtros opcionais.
    
    **Parâmetros de filtro:**
    - skip: Número de registros a pular (paginação)
    - limit: Número máximo de registros (máx 100)
    - categoria: Filtrar por categoria
    - status_filter: Filtrar por status
    - search: Buscar por título ou autor
    """
    
    query = db.query(Book)
    
    if categoria:
        query = query.filter(Book.categoria == categoria)
    
    if status_filter:
        query = query.filter(Book.status == status_filter)
    
    if search:
        query = query.filter(
            or_(
                Book.titulo.ilike(f"%{search}%"),
                Book.autor.ilike(f"%{search}%")
            )
        )
    
    return query.offset(skip).limit(limit).all()

@router.get(
    "/{book_id}",
    response_model=BookResponse,
    summary="Obter detalhes de um livro",
    description="Retorna informações completas de um livro específico"
)
async def get_book(
    book_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtém um livro específico por ID"""
    db_book = db.query(Book).filter(Book.id == book_id).first()
    
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado"
        )
    
    return db_book

@router.put(
    "/{book_id}",
    response_model=BookResponse,
    summary="Editar livro",
    description="Apenas administradores podem editar livros"
)
async def update_book(
    book_id: int,
    book_data: BookUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Atualiza informações de um livro"""
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
    return db_book

@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar livro",
    description="Apenas administradores podem deletar livros"
)
async def delete_book(
    book_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Deleta um livro do banco"""
    db_book = db.query(Book).filter(Book.id == book_id).first()
    
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado"
        )
    
    db.delete(db_book)
    db.commit()

