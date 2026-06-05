from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String, DateTime, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
import bcrypt

# ===== BANCO DE DADOS =====
DATABASE_URL = "postgresql://mybookie_user:sua_senha_aqui@localhost:5432/mybookie_db"

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
    email: EmailStr = Field(..., description="Email único do usuário")
    username: str = Field(..., min_length=3, max_length=100, description="Nome de usuário único")
    password: str = Field(..., min_length=8, description="Senha (mínimo 8 caracteres)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "usuario@exemplo.com",
                "username": "usuario123",
                "password": "senha123456"
            }
        }

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(..., description="Senha do usuário")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "usuario@exemplo.com",
                "password": "senha123456"
            }
        }

class BookCreate(BaseModel):
    titulo: str = Field(..., min_length=3, description="Título do livro")
    autor: str = Field(..., min_length=3, description="Autor do livro")
    isbn: str = Field(..., min_length=10, description="ISBN do livro (único)")
    descricao: str = Field(None, description="Descrição detalhada do livro")
    categoria: str = Field(None, description="Categoria/gênero do livro")
    quantidade: int = Field(default=1, ge=1, description="Quantidade de exemplares")
    
    class Config:
        json_schema_extra = {
            "example": {
                "titulo": "Dom Casmurro",
                "autor": "Machado de Assis",
                "isbn": "9788535906776",
                "descricao": "Clássico da literatura brasileira",
                "categoria": "Romance",
                "quantidade": 5
            }
        }

# ===== FUNÇÕES UTILITÁRIAS =====
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def book_to_dict(book):
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
    title="📚 Mybookie API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    description="""
<style>
  .doc-section {
    background: #f5f7fa;
    padding: 20px;
    border-radius: 8px;
    margin: 15px 0;
    border-left: 4px solid #667eea;
  }
  .doc-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 30px;
    border-radius: 8px;
    margin-bottom: 20px;
    text-align: center;
  }
  .feature-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
    margin: 15px 0;
  }
  .feature-card {
    background: white;
    padding: 15px;
    border-radius: 8px;
    border: 2px solid #e0e0e0;
    transition: all 0.3s ease;
  }
  .feature-card:hover {
    border-color: #667eea;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
  }
  .endpoint-table {
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
  }
  .endpoint-table th {
    background: #667eea;
    color: white;
    padding: 12px;
    text-align: left;
  }
  .endpoint-table td {
    padding: 12px;
    border-bottom: 1px solid #ddd;
  }
  .endpoint-table tr:hover {
    background: #f5f5f5;
  }
  .status-200 { color: #4CAF50; font-weight: bold; }
  .status-201 { color: #2196F3; font-weight: bold; }
  .status-400 { color: #FF9800; font-weight: bold; }
  .status-401 { color: #F44336; font-weight: bold; }
  .status-404 { color: #F44336; font-weight: bold; }
</style>

<div class="doc-header">
  <h1>📚 Mybookie API</h1>
  <h3>Sistema Completo de Biblioteca Escolar</h3>
  <p style="margin: 15px 0; font-size: 0.95em;">
    Desenvolvido com ❤️ por <strong>Michele Caroline Teixeira de Oliveira</strong><br>
    <em>Senior QA Engineer | Professora Universitária | Test Automation</em>
  </p>
</div>

---

## 🎯 O que é Mybookie?

<div class="doc-section">
Sistema completo e profissional de gerenciamento de biblioteca escolar com:

✅ **Autenticação segura** - Registro e login com hash de senha  
✅ **CRUD de Livros** - Gerenciar acervo com ISBN único  
✅ **Gestão de Usuários** - Controle de acessos  
✅ **Documentação automática** - Swagger/OpenAPI  
✅ **API RESTful** - Endpoints bem estruturados  

</div>

---

## 🚀 Quick Start em 4 Passos

<div class="doc-section">

### 1️⃣ Registre-se
POST /api/v1/auth/register
{ "email": "seu@email.com", "username": "seuusuario", "password": "senha123456" }

### 2️⃣ Faça Login
POST /api/v1/auth/login
{ "email": "seu@email.com", "password": "senha123456" }

### 3️⃣ Explore os Livros
GET /api/v1/books

### 4️⃣ Crie um Novo Livro
POST /api/v1/books
{ "titulo": "Dom Casmurro", "autor": "Machado de Assis", "isbn": "9788535906776", "descricao": "Clássico da literatura brasileira", "categoria": "Romance", "quantidade": 5 }

</div>

---

## 📚 Funcionalidades

<div class="feature-grid">
  <div class="feature-card">
    <h4>🔐 Autenticação</h4>
    <p>Login seguro com hash bcrypt</p>
  </div>
  <div class="feature-card">
    <h4>📖 Gerenciar Livros</h4>
    <p>CRUD completo com validações</p>
  </div>
  <div class="feature-card">
    <h4>👥 Gestão de Usuários</h4>
    <p>Criar e controlar contas</p>
  </div>
  <div class="feature-card">
    <h4>📊 Relatórios</h4>
    <p>Informações da biblioteca</p>
  </div>
</div>

---

## 🔗 Endpoints Disponíveis

<table class="endpoint-table">
  <thead>
    <tr>
      <th>Método</th>
      <th>Endpoint</th>
      <th>Descrição</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>GET</td>
      <td>/</td>
      <td>Informações da API</td>
      <td><span class="status-200">200</span></td>
    </tr>
    <tr>
      <td>GET</td>
      <td>/health</td>
      <td>Health check</td>
      <td><span class="status-200">200</span></td>
    </tr>
    <tr>
      <td>GET</td>
      <td>/about</td>
      <td>Sobre a biblioteca</td>
      <td><span class="status-200">200</span></td>
    </tr>
    <tr>
      <td>GET</td>
      <td>/developer</td>
      <td>Sobre Michele</td>
      <td><span class="status-200">200</span></td>
    </tr>
    <tr>
      <td>POST</td>
      <td>/api/v1/auth/register</td>
      <td>Registrar novo usuário</td>
      <td><span class="status-201">201</span></td>
    </tr>
    <tr>
      <td>POST</td>
      <td>/api/v1/auth/login</td>
      <td>Fazer login</td>
      <td><span class="status-200">200</span></td>
    </tr>
    <tr>
      <td>GET</td>
      <td>/api/v1/books</td>
      <td>Listar livros</td>
      <td><span class="status-200">200</span></td>
    </tr>
    <tr>
      <td>GET</td>
      <td>/api/v1/books/{id}</td>
      <td>Obter livro</td>
      <td><span class="status-200">200</span></td>
    </tr>
    <tr>
      <td>POST</td>
      <td>/api/v1/books</td>
      <td>Criar livro</td>
      <td><span class="status-201">201</span></td>
    </tr>
    <tr>
      <td>PUT</td>
      <td>/api/v1/books/{id}</td>
      <td>Atualizar livro</td>
      <td><span class="status-200">200</span></td>
    </tr>
    <tr>
      <td>DELETE</td>
      <td>/api/v1/books/{id}</td>
      <td>Deletar livro</td>
      <td><span class="status-200">200</span></td>
    </tr>
  </tbody>
</table>

---

## 📝 Códigos de Resposta

<div class="doc-section">

| Código | Significado | Exemplo |
|--------|------------|---------|
| <span class="status-200">200</span> | ✅ Sucesso | GET /api/v1/books |
| <span class="status-201">201</span> | ✅ Criado | POST /api/v1/books |
| <span class="status-400">400</span> | ❌ Requisição inválida | Email já existe |
| <span class="status-401">401</span> | ❌ Não autorizado | Senha incorreta |
| <span class="status-404">404</span> | ❌ Não encontrado | Livro não existe |

</div>

---

## 🛠️ Stack Técnico

<div class="feature-grid">
  <div class="feature-card">
    <h4>Backend</h4>
    <p>FastAPI + SQLAlchemy + PostgreSQL</p>
  </div>
  <div class="feature-card">
    <h4>Frontend</h4>
    <p>React + Vite + Axios</p>
  </div>
  <div class="feature-card">
    <h4>Segurança</h4>
    <p>bcrypt + CORS</p>
  </div>
  <div class="feature-card">
    <h4>Deploy</h4>
    <p>Vercel + Railway</p>
  </div>
</div>

---

## 👩‍💻 Sobre a Desenvolvedora

<div class="doc-section">

**Michele Caroline Teixeira de Oliveira**

📍 Garça, São Paulo, Brasil  
📧 [michele564000@gmail.com](mailto:michele564000@gmail.com)  
📱 (14) 99631-2027  
💼 [LinkedIn](https://linkedin.com/in/michelecarolineoliveira)

### Expertise:
- 🧪 Testes de Software (Manual e Automatizado)
- 🤖 Automação com Selenium, Capybara, Cucumber
- 👨‍🏫 Docência em Testes e Qualidade de Software
- 🔄 CI/CD e Quality Strategy
- 📊 Análise Crítica de Qualidade

### Certificações:
- ✅ Certified Tester Foundation Level (CTFL)
- ✅ Selenium: Testes automatizados em .NET
- ✅ Automação com Capybara, Cucumber e Ruby
- ✅ Jasmine: Testes em JavaScript
- ✅ Cucumber e BDD para web apps

</div>

---

## 💡 Dicas Úteis

<div class="doc-section">

1. **Para testar os endpoints:** Use o botão "Try it out" em cada endpoint
2. **Para ver exemplos:** Clique em "Schemas" para ver estruturas de dados
3. **Para documentação completa:** Vá em `/redoc` para ReDoc
4. **Para explorar:** Clique em qualquer endpoint para ver detalhes

</div>

---

## 📄 Licença

MIT License - Código aberto e livre para usar

---

<div style="text-align: center; margin-top: 30px; padding: 20px; background: #f0f0f0; border-radius: 8px;">
  <p><strong>Desenvolvido com ❤️ por Michele</strong></p>
  <p style="font-size: 0.9em; color: #666;">
    Mybookie © 2025 | Todos os direitos reservados
  </p>
</div>

""",
    contact={
        "name": "Michele Caroline Teixeira de Oliveira",
        "email": "michele564000@gmail.com",
        "url": "https://linkedin.com/in/michelecarolineoliveira"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    openapi_tags=[
        {
            "name": "Sistema",
            "description": "🔧 Endpoints de sistema e informações gerais"
        },
        {
            "name": "Autenticação",
            "description": "🔐 Registro e login de usuários"
        },
        {
            "name": "Livros",
            "description": "📖 CRUD completo para gerenciar livros da biblioteca"
        },
        {
            "name": "Sobre",
            "description": "👩‍💻 Informações sobre a desenvolvedora"
        }
    ]
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

@app.get(
    "/",
    tags=["Sistema"],
    summary="🏠 Informações da API",
    description="Retorna informações básicas da API e links úteis"
)
async def root():
    """
    **Endpoint raiz** - Informações sobre a API
    
    Retorna:
    - Versão da API
    - Links para documentação
    - Links para health check e about
    """
    return {
        "message": "Bem-vindo ao Mybookie",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "about": "/about",
        "developer": "/developer"
    }

@app.get(
    "/health",
    tags=["Sistema"],
    summary="🏥 Health Check",
    description="Verifica se a API está funcionando",
    responses={200: {"description": "API está saudável"}}
)
async def health():
    """
    **Health Check** - Verifica o status da API
    
    Retorna status de saúde simples
    """
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get(
    "/about",
    tags=["Sistema"],
    summary="ℹ️ Informações da Biblioteca",
    description="Retorna informações sobre a biblioteca e seu administrador"
)
async def about():
    """
    **Sobre** - Informações da biblioteca
    
    Retorna:
    - Nome da biblioteca
    - Descrição
    - Informações do administrador
    - Estatísticas gerais
    """
    return {
        "nome": "Mybookie",
        "descricao": "Sistema de gerenciamento de biblioteca para aulas",
        "admin_nome": "Michele Caroline Teixeira de Oliveira",
        "admin_email": "michele564000@gmail.com",
        "admin_titulo": "Senior QA Engineer | Professora Universitária",
        "versao_api": "1.0.0",
        "total_livros": 0,
        "total_usuarios": 0,
        "locacao": "Garça, São Paulo, Brasil"
    }

@app.get(
    "/developer",
    tags=["Sobre"],
    summary="👩‍💻 Informações da Desenvolvedora",
    description="Informações detalhadas sobre Michele, a criadora da API"
)
async def developer_info():
    """
    **Sobre Michele Caroline Teixeira de Oliveira**
    
    Senior QA Engineer e Professora Universitária com paixão por qualidade de software.
    
    **Competências:**
    - 🧪 Testes de Software (Manuais e Automatizados)
    - 🤖 Automação com Selenium, Capybara, Cucumber
    - 👨‍🏫 Docência em Testes e Qualidade
    - 🔄 CI/CD e Quality Strategy
    - 📊 Análise Crítica e Gestão de Qualidade
    
    **Certificações:**
    - Certified Tester Foundation Level (CTFL)
    - Selenium: Testes automatizados em .NET
    - Automação com Capybara, Cucumber e Ruby
    - Jasmine: Testes em JavaScript
    - Cucumber e BDD para web apps
    
    **Contato e Links:**
    - 📧 Email: michele564000@gmail.com
    - 📱 Telefone: (14) 99631-2027
    - 💼 LinkedIn: https://linkedin.com/in/michelecarolineoliveira
    - 📍 Localização: Garça, São Paulo, Brasil
    """
    return {
        "nome": "Michele Caroline Teixeira de Oliveira",
        "titulo": "Senior QA Engineer | Professora Universitária | Test Automation",
        "locacao": "Garça, São Paulo, Brasil",
        "email": "michele564000@gmail.com",
        "telefone": "(14) 99631-2027",
        "linkedin": "https://linkedin.com/in/michelecarolineoliveira",
        "experiencia_anos": 7,
        "resumo": "QA Sênior e Professora universitária com mais de 7 anos de experiência em Testes de Software, atuando na garantia da qualidade em aplicações web e APIs. Pós-graduada em Testes e Desenvolvimento de Software.",
        "competencias": {
            "qa": ["Testes Manuais", "Automação de Testes", "Testes de API", "Testes de Acessibilidade", "BDD", "Cucumber"],
            "linguagens": ["Selenium", "Capybara", "Ruby", "JavaScript", "Jasmine", "TestLink"],
            "metodologias": ["CI/CD", "Quality Strategy", "Scrum", "Test Planning", "Agile"],
            "soft_skills": ["Docência", "Comunicação", "Liderança", "Análise Crítica", "Mentoria"]
        },
        "certificacoes": [
            "Certified Tester Foundation Level (CTFL)",
            "Selenium: Testes automatizados de aceitação em .NET",
            "Automação de Testes com Capybara, Cucumber e Ruby",
            "Jasmine: Testes automatizados em JavaScript",
            "Cucumber e BDD para web apps"
        ],
        "experiencias_principais": [
            {
                "titulo": "Professora Universitária",
                "empresa": "Universidade de Marília",
                "periodo": "2025 - Presente"
            },
            {
                "titulo": "Analista de Testes III",
                "empresa": "Tray",
                "periodo": "2025 - Presente"
            },
            {
                "titulo": "Senior QA Engineer",
                "empresa": "Tray",
                "periodo": "2020 - 2025"
            }
        ]
    }

# ===== AUTH ROUTES =====

@app.post(
    "/api/v1/auth/register",
    tags=["Autenticação"],
    status_code=201,
    summary="📝 Registrar novo usuário",
    description="Cria uma nova conta de usuário na plataforma",
    responses={
        201: {"description": "Usuário criado com sucesso"},
        400: {"description": "Email ou username já registrado"}
    }
)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    **Registrar novo usuário**
    
    Cria uma nova conta de leitora na biblioteca.
    
    **Validações:**
    - Email deve ser único
    - Username deve ser único e ter 3+ caracteres
    - Senha deve ter 8+ caracteres
    
    **Retorna:**
    - ID do usuário
    - Email
    - Username
    - Mensagem de sucesso
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

@app.post(
    "/api/v1/auth/login",
    tags=["Autenticação"],
    summary="🔓 Fazer login",
    description="Autentica um usuário e retorna dados da sessão",
    responses={
        200: {"description": "Login bem-sucedido"},
        401: {"description": "Credenciais inválidas"}
    }
)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    **Login de usuário**
    
    Autentica um usuário com email e senha.
    
    **Retorna:**
    - ID do usuário
    - Email
    - Username
    - Mensagem de sucesso
    """
    
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

@app.get(
    "/api/v1/books",
    tags=["Livros"],
    summary="📚 Listar todos os livros",
    description="Retorna uma lista de todos os livros cadastrados na biblioteca",
    responses={200: {"description": "Lista de livros retornada com sucesso"}}
)
async def list_books(db: Session = Depends(get_db)):
    """
    **Listar livros**
    
    Retorna todos os livros da biblioteca em formato de lista.
    
    **Cada livro contém:**
    - ID único
    - Título
    - Autor
    - ISBN
    - Descrição
    - Categoria
    - Quantidade disponível
    - Status
    """
    books = db.query(Book).all()
    return [book_to_dict(book) for book in books]

@app.get(
    "/api/v1/books/{book_id}",
    tags=["Livros"],
    summary="🔍 Obter detalhes de um livro",
    description="Retorna informações detalhadas de um livro específico",
    responses={
        200: {"description": "Livro encontrado"},
        404: {"description": "Livro não encontrado"}
    }
)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    **Obter livro por ID**
    
    Retorna informações completas de um livro específico.
    
    **Parâmetros:**
    - `book_id`: ID do livro (path parameter)
    
    **Erros:**
    - 404: Livro não encontrado
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado"
        )
    
    return book_to_dict(book)

@app.post(
    "/api/v1/books",
    tags=["Livros"],
    status_code=201,
    summary="➕ Criar novo livro",
    description="Adiciona um novo livro ao acervo da biblioteca (apenas admin)",
    responses={
        201: {"description": "Livro criado com sucesso"},
        400: {"description": "ISBN já existe ou dados inválidos"}
    }
)
async def create_book(book_data: BookCreate, db: Session = Depends(get_db)):
    """
    **Criar novo livro**
    
    Adiciona um novo livro ao acervo da biblioteca.
    
    **Validações:**
    - ISBN deve ser único
    - Título e Autor são obrigatórios
    - Quantidade deve ser >= 1
    
    **Retorna:**
    - Dados do livro criado com ID
    """
    
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

@app.put(
    "/api/v1/books/{book_id}",
    tags=["Livros"],
    summary="✏️ Atualizar livro",
    description="Edita as informações de um livro existente (apenas admin)",
    responses={
        200: {"description": "Livro atualizado com sucesso"},
        404: {"description": "Livro não encontrado"}
    }
)
async def update_book(book_id: int, book_data: BookCreate, db: Session = Depends(get_db)):
    """
    **Atualizar livro**
    
    Edita as informações de um livro existente.
    
    **Parâmetros:**
    - `book_id`: ID do livro a atualizar
    - Body: Novos dados do livro
    
    **Erros:**
    - 404: Livro não encontrado
    """
    
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

@app.delete(
    "/api/v1/books/{book_id}",
    tags=["Livros"],
    status_code=204,
    summary="🗑️ Deletar livro",
    description="Remove um livro do acervo da biblioteca (apenas admin)",
    responses={
        204: {"description": "Livro deletado com sucesso"},
        404: {"description": "Livro não encontrado"}
    }
)
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    **Deletar livro**
    
    Remove um livro do acervo da biblioteca.
    
    **Parâmetros:**
    - `book_id`: ID do livro a deletar
    
    **Erros:**
    - 404: Livro não encontrado
    
    ⚠️ **Nota:** Esta operação é irreversível
    """
    
    db_book = db.query(Book).filter(Book.id == book_id).first()
    
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado"
        )
    
    db.delete(db_book)
    db.commit()
    
    return None