# 📚 Mybookie

Sistema de gerenciamento de biblioteca pessoal com autenticação, CRUD de livros e avaliações com 5 estrelas.

---

## ✨ Características

- 📖 CRUD completo de livros
- ⭐ Avaliação com 5 estrelas
- 🔍 Filtros por nome e status de leitura
- 👤 Autenticação com bcrypt
- 📱 Design responsivo
- 📚 Documentação Swagger

---

## 🛠️ Stack

**Frontend:** React 18, Vite, Axios, CSS3
**Backend:** Python, FastAPI, SQLAlchemy, PostgreSQL, Bcrypt

---

## 🚀 Instalação

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install fastapi uvicorn sqlalchemy psycopg2-binary bcrypt
uvicorn app.main:app --reload
```

Backend: `http://localhost:8000`
Docs: `http://localhost:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend: `http://localhost:5173`

---

## 📖 Como Usar

1. Registre uma conta
2. Faça login
3. Adicione livros com título, autor e categoria
4. Marque como lido e deixe sua avaliação
5. Filtre e pesquise seus livros

---

## 🔌 API Endpoints
POST /api/v1/auth/register - Registrar POST /api/v1/auth/login - Fazer login GET /api/v1/books - Listar livros POST /api/v1/books - Criar livro PUT /api/v1/books/{id} - Atualizar livro DELETE /api/v1/books/{id} - Deletar livro GET /docs - Documentação API

---

## 👩‍💻 Autor

**Michele Caroline Teixeira de Oliveira**
- 📧 michele564000@gmail.com
- 💼 [LinkedIn](https://linkedin.com/in/michelecarolineoliveira)

---
