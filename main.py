import os
import sqlite3
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Configuração automática dos caminhos das pastas na sua máquina
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Monta a rota para que o navegador ache os arquivos dentro da pasta static
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

def buscar_alertas_reais():
    # Conecta diretamente no banco de dados real da sua raiz
    conexao = sqlite3.connect("sentinela_paranoa.db")
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    
    # Garante a existência da tabela com a estrutura correta de colunas
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
    
    # Busca todas as ocorrências salvas pelos testes ou agentes
    cursor.execute("SELECT categoria, posicao_top, posicao_left, descricao FROM ocorrencias")
    linhas = cursor.fetchall()
    conexao.close()
    
    # Devolve os dados formatados em dicionário para o Jinja2 processar
    return [dict(linha) for linha in linhas]

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    try:
        alertas = buscar_alertas_reais()
    except Exception as e:
        print(f"Aviso de Bancada (Erro ao ler banco): {e}")
        alertas = []
        
    return templates.TemplateResponse("index.html", {"request": request, "alerts": alertas})
