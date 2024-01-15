from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI()

# Configuração do MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["banco_site"]
collection = db["cadastro"]

# Configuração do CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:27017",
    "https://projeto-login-blond-eight.vercel.app",  # Adicione esta linha
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    nome: str
    login: str
    senha: str

@app.post("/cadastrar")
def cadastrar_usuario(usuario: User):
    novo_usuario = {
        "nome": usuario.nome,
        "login": usuario.login,
        "senha": usuario.senha
    }

    try:
        resultado = collection.insert_one(novo_usuario)
        return {"id_inserido": str(resultado.inserted_id)}
    except Exception as e:
        print(f"Erro ao cadastrar: {str(e)}")  # Adicionando log de erro no console
        raise HTTPException(status_code=500, detail=f"Erro ao cadastrar: {str(e)}")

