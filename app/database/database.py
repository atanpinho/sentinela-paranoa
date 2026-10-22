# =====================================================================
# PROJETO ARRANQUE: SENTINELA PARANOÁ
# COMPONENTE: BANCO DE DADOS (database.py)
# =====================================================================

import sqlite3
from datetime import datetime

def inicializar_banco():
    """
    Função responsável por criar o arquivo do banco de dados 
    e estruturar a tabela de ocorrências ambientais.
    """
    conexao = sqlite3.connect("sentinela_paranoa.db")
    cursor = conexao.cursor()
    
    comando_sql = """
    CREATE TABLE IF NOT EXISTS ocorrencias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        categoria TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        descricao TEXT,
        data_criacao TEXT NOT NULL
    );
    """
    
    cursor.execute(comando_sql)
    conexao.commit()
    conexao.close()
    print("Banco de dados 'sentinela_paranoa.db' inicializado com sucesso!")


def inserir_ocorrencia(categoria: str, latitude: float, longitude: float, descricao: str):
    """
    Função anatômica responsável por receber os dados de um foco de poluição
    e gravá-los permanentemente na tabela 'ocorrencias'.
    """
    # 1. Estabelecendo a conexão com o arquivo do banco
    conexao = sqlite3.connect("sentinela_paranoa.db")
    cursor = conexao.cursor()
    
    # 2. Capturando o carimbo de data e hora do momento exato do relato
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # 3. Preparando o comando de inserção com placeholders (parâmetros seguros)
    comando_sql = """
    INSERT INTO ocorrencias (categoria, latitude, longitude, descricao, data_criacao)
    VALUES (?, ?, ?, ?, ?);
    """
    
    # 4. Executando o comando e passando os valores reais nas interrogações
    cursor.execute(comando_sql, (categoria, latitude, longitude, descricao, agora))
    
    # 5. Salvando de forma definitiva no disco rígido
    conexao.commit()
    
    # 6. Fechando a comunicação com o cofre
    conexao.close()
    print(f"Sucesso: Novo alerta de '{categoria}' gravado no Sentinela!")


# Bloco de Execução de Teste do Programador
if __name__ == "__main__":
    # Garante que a tabela existe antes do teste
    inicializar_banco()
    
    print("\n--- SIMULANDO UM RELATO REAL DE CIDADÃO EM BRASÍLIA ---")
    
    # Simulando um descarte clandestino de esgoto próximo ao Córrego Taguatinga
    inserir_ocorrencia(
        categoria="Esgoto Clandestino",
        latitude=-15.8123,
        longitude=-48.0564,
        descricao="Cheiro forte de esgoto vindo da galeria pluvial perto do IFB Campus Taguatinga."
    )
