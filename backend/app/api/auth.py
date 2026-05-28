from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, LoginRequest, TokenResponse, UserResponse
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)
from app.config import get_settings

router = APIRouter(prefix="/auth", tags=["Autenticação"])
settings = get_settings()

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nova leitora",
    description="Cria uma nova conta de leitora na biblioteca"
)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Registra uma nova leitora.
    
    - **email**: Email único
    - **username**: Nome de usuário único (mín. 3 caracteres)
    - **full_name**: Nome completo (opcional)
    - **matricula**: Matrícula da aula (opcional)
    - **password**: Senha (mín. 8 caracteres)
    """
    
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
        full_name=user_data.full_name,
        matricula=user_data.matricula,
        hashed_password=hash_password(user_data.password),
        role="user"  # Sempre cria como usuário comum
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login",
    description="Faz login e retorna um JWT token"
)
async def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """
    Faz login com email e senha.
    
    Retorna um token JWT válido por 8 horas.
    """
    
    # Busca usuário por email
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário desativado"
        )
    
    # Cria token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.post(
    "/logout",
    summary="Logout",
    description="Logout (no frontend, apenas delete o token)"
)
async def logout(current_user: User = Depends(get_current_user)):
    """Logout simples - no frontend, deletar o token do localStorage"""
    return {"message": "Logout bem-sucedido"}

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Dados do usuário",
    description="Retorna dados do usuário autenticado"
)
async def get_me(current_user: User = Depends(get_current_user)):
    """Retorna dados da leitora autenticada"""
    return current_user

@router.put(
    "/me",
    response_model=UserResponse,
    summary="Atualizar perfil",
    description="Atualiza dados do perfil da leitora"
)
async def update_me(
    user_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualiza dados do perfil"""
    for field, value in user_data.items():
        if value is not None and hasattr(current_user, field):
            setattr(current_user, field, value)
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

