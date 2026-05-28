from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Mybookie",
    version="1.0.0",
    description="API de Biblioteca"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Bem-vindo ao Mybookie", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/about")
async def about():
    return {
        "nome": "Mybookie",
        "descricao": "Sistema de gerenciamento de biblioteca",
        "admin_nome": "Administrador",
        "admin_email": "admin@mybookie.com"
    }