import sqlite3

def inicializar_banco():
    """
    Função macro responsável por criar o arquivo do banco de dados 
    e estruturar as tabelas necessárias para o Sentinela Paranoá.
    """
    # Estabelece a conexão com o arquivo SQLite. Se ele não existir, será criado.
    conexao = sqlite3.connect('sentinela_paranoa.db')
    cursor = conexao.cursor()
    
    # Criação da tabela de alertas utilizando restrições de integridade
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alertas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_crime TEXT NOT NULL,
            localizacao TEXT NOT NULL,
            posicao_top REAL NOT NULL,
            posicao_left REAL NOT NULL
        )
    ''')
    
    # Validação para não duplicar o ponto inicial de teste a cada reinicialização
    cursor.execute("SELECT COUNT(*) FROM alertas")
    if cursor.fetchone()[0] == 0:
        # Inserção da semente inicial (Seed Data) correspondente ao nosso print de validação
        cursor.execute('''
            INSERT INTO alertas (tipo_crime, localizacao, posicao_top, posicao_left)
            VALUES (?, ?, ?, ?)
        ''', ('Esgoto Clandestino', 'Vila Cauí / Park Way', 61.5, 50.0))
    
    # Salva as alterações de forma permanente e fecha os recursos de rede/disco
    conexao.commit()
    conexao.close()

if __name__ == '__main__':
    inicializar_banco()
    print("Base de Dados do Sentinela Paranoá inicializada com sucesso!")
