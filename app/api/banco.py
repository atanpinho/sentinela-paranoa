from pathlib import Path
import sqlite3
import shutil
from datetime import datetime
import sys


# ==================================================
# LOCALIZAÇÃO DAS PASTAS DO PROJETO
# ==================================================

# Localiza a pasta principal do projeto.
PASTA_PROJETO = Path(__file__).resolve().parents[2]

# Caminho do banco de dados existente.
CAMINHO_BANCO = PASTA_PROJETO / "sentinela.db"

# Pasta destinada às cópias de segurança.
PASTA_BACKUPS = PASTA_PROJETO / "backups"

# Pasta onde as fotografias das ocorrências são armazenadas.
PASTA_FOTOS = PASTA_PROJETO / "app" / "static" / "fotos"


# ==================================================
# INICIALIZAÇÃO DO BANCO DE DADOS
# ==================================================

def inicializar_banco():
    """Cria as tabelas necessárias sem apagar os dados existentes."""

    conexao = sqlite3.connect(CAMINHO_BANCO)

    try:
        cursor = conexao.cursor()

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


# ==================================================
# CÓPIA DE SEGURANÇA DO PROJETO
# ==================================================

def criar_backup():
    """
    Cria uma cópia de segurança do banco de dados
    e das fotografias das ocorrências ambientais.
    """

    # Verifica se o banco de dados existe.
    if not CAMINHO_BANCO.exists():
        raise FileNotFoundError(
            f"Banco de dados não encontrado: {CAMINHO_BANCO}"
        )

    # Verifica se a pasta de fotografias existe.
    if not PASTA_FOTOS.exists():
        raise FileNotFoundError(
            f"Pasta de fotografias não encontrada: {PASTA_FOTOS}"
        )

    # Cria a pasta principal de backups.
    PASTA_BACKUPS.mkdir(parents=True, exist_ok=True)

    # Gera um identificador com data, hora e microssegundos.
    data_hora = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    # Cria uma pasta exclusiva para esta cópia.
    pasta_backup = PASTA_BACKUPS / f"sentinela_{data_hora}"
    pasta_backup.mkdir(parents=True, exist_ok=False)

    # Define o destino do banco de dados copiado.
    caminho_backup_banco = pasta_backup / "sentinela.db"

    conexao_origem = None
    conexao_backup = None

    try:
        # Abre o banco de dados original.
        conexao_origem = sqlite3.connect(
            str(CAMINHO_BANCO),
            timeout=10,
        )

        # Cria o banco de dados de destino.
        conexao_backup = sqlite3.connect(
            str(caminho_backup_banco)
        )

        # Utiliza o mecanismo próprio de backup do SQLite.
        conexao_origem.backup(conexao_backup)

        # Fecha as conexões antes de continuar.
        conexao_backup.close()
        conexao_backup = None

        conexao_origem.close()
        conexao_origem = None

        # Define a pasta de fotografias dentro do backup.
        destino_fotos = pasta_backup / "fotos"

        # Copia todas as fotografias e subpastas.
        shutil.copytree(
            PASTA_FOTOS,
            destino_fotos,
        )

    except Exception:
        # Garante o fechamento das conexões antes da limpeza.
        if conexao_backup is not None:
            conexao_backup.close()

        if conexao_origem is not None:
            conexao_origem.close()

        # Remove a pasta incompleta para evitar backup parcial.
        if pasta_backup.exists():
            shutil.rmtree(pasta_backup)

        raise

    return pasta_backup


# ==================================================
# EXECUÇÃO DIRETA DESTE ARQUIVO
# ==================================================

if __name__ == "__main__":

    # Cria o backup somente quando o comando --backup é informado.
    if "--backup" in sys.argv:
        caminho_backup = criar_backup()

        print("Backup criado com sucesso!")
        print(f"Local: {caminho_backup}")

    else:
        # Mantém o comportamento anterior de inicialização do banco.
        inicializar_banco()

        print("Banco de dados inicializado com sucesso!")
        print(f"Local do banco: {CAMINHO_BANCO}")