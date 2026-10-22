# =====================================================================
# PROJETO ARRANQUE: SENTINELA PARANOÁ
# COMPONENTE: CONEXÃO E ROTAS DA API (main.py)
# =====================================================================

import sqlite3
from fastapi import FastAPI

# 1. Instanciando o cérebro da nossa aplicação web
app = FastAPI(
    title="ARRANQUE: Sentinela Paranoá API",
    description="Interface de comunicação para monitoramento ecológico dos córregos de Brasília."
)

@app.get("/")
def ler_raiz():
    """
    Rota inicial de boas-vidas para testar se o servidor está online.
    """
    return {"status": "online", "projeto": "Sentinela Paranoá"}


@app.get("/ocorrencias")
def listar_ocorrencias():
    """
    Rota anatômica encarregada de buscar os relatos de poluição
    guardados no banco de dados e entregá-los formatados para a internet.
    """
    # Estabelecendo conexão para leitura com o arquivo do banco
    conexao = sqlite3.connect("sentinela_paranoa.db")
    
    # Ativando o recurso que transforma as linhas brutas em dicionários legíveis
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    
    # Buscando todos os registros salvos na tabela ocorrencias
    cursor.execute("SELECT * FROM ocorrencias;")
    linhas = cursor.fetchall()
    
    # Fechando a conexão para liberar o arquivo do banco
    conexao.close()
    
    # Transformando o resultado em um formato padrão de mercado (JSON)
    resultado = [dict(linha) for linha in linhas]
    return resultado
