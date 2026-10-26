from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import sqlite3
import os

app = FastAPI()

# Configura o motor do Jinja2 apontando para a pasta templates na raiz do projeto
templates = Jinja2Templates(directory="templates")

# Define o caminho absoluto para o banco de dados na raiz do projeto
CAMINHO_BANCO = os.path.join(os.getcwd(), 'sentinela_paranoa.db')

def garantir_banco_e_dados():
    """Garante que a tabela estrutural e o primeiro ponto ecológico existam."""
    conexao = sqlite3.connect(CAMINHO_BANCO)
    cursor = conexao.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alertas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_crime TEXT NOT NULL,
            localizacao TEXT NOT NULL,
            posicao_top REAL NOT NULL,
            posicao_left REAL NOT NULL
        )
    ''')
    
    cursor.execute("SELECT COUNT(*) FROM alertas")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO alertas (tipo_crime, localizacao, posicao_top, posicao_left)
            VALUES (?, ?, ?, ?)
        ''', ('Esgoto Clandestino', 'Vila Cauí / Park Way', 61.5, 50.0))
        
    conexao.commit()
    conexao.close()

def buscar_alertas_no_banco():
    """Conecta ao SQLite e extrai as linhas catalogadas do Lago Paranoá."""
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    
    cursor.execute("SELECT tipo_crime, localizacao, posicao_top, posicao_left FROM alertas")
    alertas_registrados = cursor.fetchall()
    
    conexao.close()
    return alertas_registrados

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Gerencia a rota principal montando o contexto de dados isolado."""
    garantir_banco_e_dados()
    dados_dos_alertas = buscar_alertas_no_banco()
    
    # Contexto explicitamente montado com chaves de dicionário {}
    contexto = {
        "request": request,
        "alertas": dados_dos_alertas
    }
    
    return templates.TemplateResponse("index.html", contexto)
