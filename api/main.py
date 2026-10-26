import os
import sqlite3
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Configuração de caminhos e templates baseados no diretório atual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "../templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "../static")), name="static")

CAMINHO_BANCO = os.path.join(BASE_DIR, "../sentinela_paranoa.db")

def garantir_banco_e_dados():
    """Garante que a tabela exista e insere dados fictícios se estiver vazia."""
    conexao = sqlite3.connect(CAMINHO_BANCO)
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alertas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_crime TEXT NOT NULL,
            localizacao TEXT NOT NULL,
            posicao_top REAL NOT NULL,
            posicao_left REAL NOT NULL
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM alertas")
    resultado = cursor.fetchone()
    if resultado and resultado[0] == 0:
        dados_iniciais = [
            ("Esgoto Clandestino", "Vila Cauhy", 61.5, 50.0),
            ("Descarte de Lixo", "Margem Norte", 40.0, 75.2),
            ("Desmatamento Irregular", "Afluente Leste", 25.4, 30.1)
        ]
        cursor.executemany("""
            INSERT INTO alertas (tipo_crime, localizacao, posicao_top, posicao_left)
            VALUES (?, ?, ?, ?)
        """, dados_iniciais)
        conexao.commit()
    conexao.close()

def buscar_alertas_no_banco():
    """Conecta ao SQLite e extrai as linhas do banco como dicionários puros do Python."""
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    cursor.execute("SELECT tipo_crime, localizacao, posicao_top, posicao_left FROM alertas")
    alertas_registrados = cursor.fetchall()
    
    lista_alertas = [dict(linha) for linha in alertas_registrados]
    
    conexao.close()
    return lista_alertas

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Gerencia a rota principal montando o contexto de dados enviado ao template."""
    garantir_banco_e_dados()
    dados_dos_alertas = buscar_alertas_no_banco()
    
    return templates.TemplateResponse("index.html", {"request": request, "alertas": dados_dos_alertas})
