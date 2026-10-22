# =====================================================================
# PROJETO ARRANQUE: SENTINELA PARANOÁ
# COMPONENTE: BANCO DE DADOS (database.py)
# =====================================================================

import sqlite3

def inicializar_banco():
    """
    Função responsável por criar o arquivo do banco de dados 
    e estruturar a tabela de ocorrências ambientais.
    """
    # 1. Conexão com o arquivo do banco de dados
    conexao = sqlite3.connect("sentinela_paranoa.db")
    
    # 2. Criação do cursor (o executor de comandos)
    cursor = conexao.cursor()
    
    # 3. Escrita do comando SQL para criar a tabela
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
    
    # 4. Executando o comando no banco de dados
    cursor.execute(comando_sql)
    
    # 5. Salvando as alterações de forma permanente
    conexao.commit()
    
    # 6. Fechando a conexão para liberar memória do sistema
    conexao.close()
    print("Banco de dados 'sentinela_paranoa.db' inicializado com sucesso!")

# Executa a função caso o arquivo seja rodado diretamente no terminal
if __name__ == "__main__":
    inicializar_banco()
    
