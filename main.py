import os
import sqlite3
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Configuração fixa de caminhos físicos da prancheta
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

def buscar_alertas_reais():
    """Busca as ocorrências gravadas no arquivo físico de banco"""
    conexao = sqlite3.connect("sentinela_paranoa.db")
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ocorrencias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        categoria TEXT NOT NULL,
        posicao_top REAL NOT NULL,
        posicao_left REAL NOT NULL,
        descricao TEXT,
        data_registro DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conexao.commit()
    
    cursor.execute("SELECT categoria, posicao_top, posicao_left, descricao FROM ocorrencias")
    linhas = cursor.fetchall()
    conexao.close()
    
    return [dict(linha) for linha in linhas]

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Rota raiz que serve a prancheta visual com os marcadores"""
    try:
        alertas = buscar_alertas_reais()
    except Exception as e:
        print(f"Aviso de Bancada: {e}")
        alertas = []
        
    # CORREÇÃO DEFINITIVA: Passando o request como primeiro argumento para sanar o erro de tupla
    return templates.TemplateResponse(request, "index.html", {"alerts": alertas})
