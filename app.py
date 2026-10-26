import os
import sqlite3
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Configuração da pasta de arquivos estáticos (para ler o mapa)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
pasta_static = os.path.join(BASE_DIR, "static")
if not os.path.exists(pasta_static):
    os.makedirs(pasta_static)
app.mount("/static", StaticFiles(directory=pasta_static), name="static")

CAMINHO_BANCO = os.path.join(BASE_DIR, "sentinela_paranoa.db")

def inicializar_sistema():
    """Garante a criação do banco limpo e insere os dados iniciais."""
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
    if cursor.fetchone()[0] == 0:
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

def coletar_alertas():
    """Busca os alertas no SQLite de forma direta."""
    conexao = sqlite3.connect(CAMINHO_BANCO)
    cursor = conexao.cursor()
    cursor.execute("SELECT tipo_crime, localizacao, posicao_top, posicao_left FROM alertas")
    linhas = cursor.fetchall()
    conexao.close()
    return linhas

@app.get("/", response_class=HTMLResponse)
async def pagina_principal(request: Request):
    inicializar_sistema()
    alertas = coletar_alertas()
    
    # Gerando os marcadores dinamicamente de forma segura via string template
    blocos_alertas = ""
    for a in alertas:
        blocos_alertas += f"""
        <div class="marcador-alerta" style="top: {a[2]}%; left: {a[3]}%;">
            ⚠️ {a[0]}<br>
            <span>{a[1]}</span>
        </div>
        """

    html_conteudo = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ARRANQUE - Sentinela Paranoá</title>
        <style>
            body {{ margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4; overflow-x: hidden; }}
            #painel-mapa {{ display: flex; flex-direction: column; align-items: center; width: 100%; }}
            #topo {{ background-color: #0b5147; color: white; text-align: center; padding: 15px 20px; width: 100%; box-sizing: border-box; z-index: 10; }}
            #topo h2 {{ margin: 0 0 5px 0; font-size: 24px; }}
            #topo p {{ margin: 0; font-size: 14px; opacity: 0.9; }}
            #area-conteudo {{ position: relative; width: 100vw; margin: 0; padding: 0; }}
            .mapa-local {{ display: block; width: 100%; height: auto; }}
            .marcador-alerta {{ position: absolute; background-color: #d32f2f; color: white; padding: 8px 14px; border-radius: 4px; font-weight: bold; font-size: 14px; box-shadow: 0px 3px 6px rgba(0,0,0,0.3); white-space: nowrap; transform: translate(-50%, -50%); font-family: sans-serif; }}
            .marcador-alerta span {{ font-size: 12px; font-weight: normal; color: #ffcdd2; display: inline-block; margin-top: 2px; }}
        </style>
    </head>
    <body>
        <div id="painel-mapa">
            <div id="topo">
                <h2>🚀 ARRANQUE: Sentinela Paranoá</h2>
                <p>Monitoramento Ecológico da Bacia Hidrográfica do Lago Paranoá</p>
            </div>
            <div id="area-conteudo">
                <img class="mapa-local" src="/static/mapa_oficial_gdf.png" alt="Mapa Oficial GDF Local">
                {blocos_alertas}
            </div>
        </div>
    </body>
    </html>
    """
    return html_conteudo
