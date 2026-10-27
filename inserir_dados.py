# =====================================================================
# PROJETO ARRANQUE: SENTINELA PARANOÁ
# COMPONENTE: SCRIPT DE TESTE DE INSERÇÃO (inserir_dados.py)
# =====================================================================

import sqlite3
from datetime import datetime

def simular_denuncia_comunidade(categoria, posicao_top, posicao_left, descricao):
    """
    Função anatômica responsável por conectar ao banco na raiz,
    garantir a existência da tabela e gravar a ocorrência de forma segura.
    """
    # 1. Conectando diretamente ao arquivo físico localizado na raiz
    conexao = sqlite3.connect("sentinela_paranoa.db")
    cursor = conexao.cursor()
    
    # 2. PASSO DE SEGURANÇA: Garante a criação da tabela se ela não existir
    # Tradução: CREATE TABLE IF NOT EXISTS = Crie a tabela se ela não existir
    comando_estrutura = """
    CREATE TABLE IF NOT EXISTS ocorrencias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        categoria TEXT NOT NULL,
        posicao_top REAL NOT NULL,
        posicao_left REAL NOT NULL,
        descricao TEXT,
        data_criacao TEXT NOT NULL
    );
    """
    cursor.execute(comando_estrutura)
    
    # 3. Registrando o carimbo de data/hora atual formatado
    data_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 4. Comando SQL parametrizado com interrogações para segurança absoluta
    comando_sql = """
    INSERT INTO ocorrencias (categoria, posicao_top, posicao_left, descricao, data_criacao)
    VALUES (?, ?, ?, ?, ?);
    """
    
    # 5. Executando e acoplando as variáveis reais nos espaços reservados
    cursor.execute(comando_sql, (categoria, posicao_top, posicao_left, descricao, data_registro))
    
    # 6. Gravando de forma permanente no disco rígido (HD/SSD)
    conexao.commit()
    
    # 7. Fechando a linha de comunicação de forma limpa
    conexao.close()
    print(f"Éxito: Tabela verificada e ponto de '{categoria}' inserido com sucesso!")

# Execução direta para teste de fumaça (Smoke Test)
if __name__ == "__main__":
    print("--- Iniciando Gravação de Teste na Raiz do Projeto ---")
    
    # Simulando um descarte ilegal de entulho próximo à bacia do Bananal
    simular_denuncia_comunidade(
        categoria="Lixo nas Margens",
        posicao_top=35.4,
        posicao_left=58.2,
        descricao="Acúmulo de entulho e plásticos descartados irregularmente na encosta do córrego."
    )
