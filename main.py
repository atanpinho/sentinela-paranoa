import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Configuração de caminhos simplificada e direta
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Cria as pastas necessárias automaticamente se não existirem
os.makedirs(os.path.join(BASE_DIR, "static"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "templates"), exist_ok=True)

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Injetando os dados direto aqui de forma segura e limpa, sem banco de dados para não travar
    dados_dos_alertas = [
        {"tipo_crime": "Esgoto Clandestino", "localizacao": "Vila Cauhy", "posicao_top": 61.5, "posicao_left": 50.0},
        {"tipo_crime": "Descarte de Lixo", "localizacao": "Margem Norte", "posicao_top": 40.0, "posicao_left": 75.2},
        {"tipo_crime": "Desmatamento Irregular", "localizacao": "Afluente Leste", "posicao_top": 25.4, "posicao_left": 30.1}
    ]
    return templates.TemplateResponse("index.html", {"request": request, "alertas": dados_dos_alertas})
