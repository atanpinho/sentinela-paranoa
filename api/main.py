import sqlite3
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="ARRANQUE: Sentinela Paranoá API",
    description="Interface de comunicação para monitoramento ecológico dos córregos de Brasília."
)

class OcorrenciaEsquema(BaseModel):
    categoria: str
    latitude: float
    longitude: float
    descricao: str

@app.get("/")
def ler_raiz():
    return {"status": "online", "projeto": "Sentinela Paranoá"}

@app.get("/ocorrencias")
def listar_ocorrencias():
    conexao = sqlite3.connect("sentinela_paranoa.db")
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM ocorrencias;")
    linhas = cursor.fetchall()
    conexao.close()
    resultado = [dict(linha) for linha in linhas]
    return resultado

@app.post("/ocorrencias")
def criar_ocorrencia(dados: OcorrenciaEsquema):
    conexao = sqlite3.connect("sentinela_paranoa.db")
    cursor = conexao.cursor()
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    comando_sql = """
    INSERT INTO ocorrencias (categoria, latitude, longitude, descricao, data_criacao)
    VALUES (?, ?, ?, ?, ?);
    """
    cursor.execute(comando_sql, (dados.categoria, dados.latitude, dados.longitude, dados.descricao, agora))
    conexao.commit()
    conexao.close()
    return {"mensagem": "Sucesso: Relato gravado com segurança no Sentinela!"}
