
from pathlib import Path
import sqlite3


# Localiza a pasta principal do projeto.
PASTA_PROJETO = Path(__file__).resolve().parents[2]


# Caminho do banco de dados existente.
CAMINHO_BANCO = PASTA_PROJETO / "sentinela.db"


def inicializar_banco():
    """Cria as tabelas necessárias sem apagar os dados existentes."""

    conexao = sqlite3.connect(CAMINHO_BANCO)

    try:
        cursor = conexao.cursor()

        # ==================================================
        # TABELA DE OCORRÊNCIAS AMBIENTAIS
        # ==================================================

        # Cria a tabela somente se ela ainda não existir.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ocorrencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_ocorrencia TEXT NOT NULL,
                descricao TEXT NOT NULL,
                local TEXT NOT NULL,
                data_registro TEXT NOT NULL
            )
        """)

        # Descobre as colunas que já existem na tabela.
        cursor.execute("PRAGMA table_info(ocorrencias)")

        colunas_existentes = {
            coluna[1]
            for coluna in cursor.fetchall()
        }

        # Adiciona somente as colunas que ainda não existem.
        novas_colunas = {
            "latitude": "REAL",
            "longitude": "REAL",
            "precisao_metros": "REAL",
            "data_captura": "TEXT",
            "foto": "TEXT",
        }

        for nome_coluna, tipo_coluna in novas_colunas.items():
            if nome_coluna not in colunas_existentes:
                cursor.execute(
                    f"ALTER TABLE ocorrencias "
                    f"ADD COLUMN {nome_coluna} {tipo_coluna}"
                )

        # ==================================================
        # TABELA DE COMENTÁRIOS DA COMUNIDADE
        # ==================================================

        # Cria uma tabela independente para os comentários.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comentarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                mensagem TEXT NOT NULL,
                data_registro TEXT NOT NULL
            )
        """)

        # Salva as alterações no banco de dados.
        conexao.commit()

    except Exception:
        # Desfaz as alterações em caso de erro.
        conexao.rollback()
        raise

    finally:
        # Fecha a conexão com o banco.
        conexao.close()


if __name__ == "__main__":
    inicializar_banco()

    print("Banco de dados inicializado com sucesso!")
    print(f"Local do banco: {CAMINHO_BANCO}")
