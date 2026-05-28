from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import User, Book
from app.schemas import StatisticsResponse, BibliotecaInfoResponse
from app.auth import get_current_admin
from app.config import get_settings

router = APIRouter(prefix="/admin", tags=["Administração"])
settings = get_settings()

@router.get(
    "/statistics",
    response_model=StatisticsResponse,
    summary="Estatísticas da biblioteca",
    description="Retorna estatísticas gerais da biblioteca"
)
async def get_statistics(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Retorna estatísticas da biblioteca"""
    
    total_livros = db.query(func.count(Book.id)).scalar()
    total_usuarios = db.query(func.count(User.id)).filter(User.role == "user").scalar()
    livros_disponiveis = db.query(func.count(Book.id)).filter(
        Book.status == "disponivel"
    ).scalar()
    livros_indisponiveis = db.query(func.count(Book.id)).filter(
        Book.status != "disponivel"
    ).scalar()
    
    return {
        "total_livros": total_livros,
        "total_usuarios": total_usuarios,
        "livros_disponiveis": livros_disponiveis,
        "livros_indisponiveis": livros_indisponiveis,
        "categoria_mais_populares": []
    }

@router.get(
    "/usuarios",
    summary="Listar usuários",
    description="Retorna lista de todas as leitoras"
)
async def list_users(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Lista todas as leitoras"""
    users = db.query(User).filter(User.role == "user").all()
    return users

@router.delete(
    "/usuarios/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar usuário",
    description="Remove uma leitora do sistema"
)
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Deleta um usuário"""
    
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não pode deletar a si mesmo"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    db.delete(user)
    db.commit()

