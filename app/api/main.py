from pathlib import Path
import sqlite3
from datetime import datetime, timezone
from uuid import uuid4
from io import BytesIO
import math

from fastapi import FastAPI, Form, Request, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image

from app.api.banco import CAMINHO_BANCO, inicializar_banco


# Localização das pastas do projeto
PASTA_PROJETO = Path(__file__).resolve().parents[2]
PASTA_TEMPLATES = PASTA_PROJETO / "app" / "templates"
PASTA_STATIC = PASTA_PROJETO / "app" / "static"
PASTA_FOTOS = PASTA_STATIC / "fotos"


# Criação da aplicação
app = FastAPI(title="Sentinela Paranoá")

templates = Jinja2Templates(directory=str(PASTA_TEMPLATES))

app.mount(
    "/static",
    StaticFiles(directory=str(PASTA_STATIC)),
    name="static",
)


def obter_conexao():
    """Abre uma conexão com o banco de dados."""
    conexao = sqlite3.connect(str(CAMINHO_BANCO), timeout=10)
    conexao.row_factory = sqlite3.Row
    return conexao


def buscar_ocorrencias():
    """Busca todas as ocorrências, da mais recente para a mais antiga."""
    conexao = obter_conexao()

    try:
        return conexao.execute(
            """
            SELECT
                id,
                tipo_ocorrencia,
                descricao,
                local,
                data_registro,
                latitude,
                longitude,
                precisao_metros,
                data_captura,
                foto
            FROM ocorrencias
            ORDER BY id DESC
            """
        ).fetchall()
    finally:
        conexao.close()


def buscar_comentarios():
    """Busca os comentários, começando pelos mais recentes."""
    conexao = obter_conexao()

    try:
        return conexao.execute(
            """
            SELECT
                id,
                nome,
                mensagem,
                data_registro
            FROM comentarios
            ORDER BY id DESC
            """
        ).fetchall()
    finally:
        conexao.close()


@app.get("/", response_class=HTMLResponse)
def pagina_inicial(request: Request):
    """Exibe o painel principal, o mapa e os comentários."""

    inicializar_banco()

    ocorrencias = buscar_ocorrencias()
    comentarios = buscar_comentarios()

    ocorrencias_com_gps = [
        {
            "id": ocorrencia["id"],
            "tipo_ocorrencia": ocorrencia["tipo_ocorrencia"],
            "descricao": ocorrencia["descricao"],
            "local": ocorrencia["local"],
            "latitude": ocorrencia["latitude"],
            "longitude": ocorrencia["longitude"],
            "data_registro": ocorrencia["data_registro"],
        }
        for ocorrencia in ocorrencias
        if ocorrencia["latitude"] is not None
        and ocorrencia["longitude"] is not None
    ]

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "ocorrencias": ocorrencias,
            "ocorrencias_com_gps": ocorrencias_com_gps,
            "comentarios": comentarios,
        },
    )


# Nova rota: Política de Privacidade
@app.get("/politica-privacidade", response_class=HTMLResponse)
def pagina_politica_privacidade(request: Request):
    """Exibe a Política de Privacidade do projeto."""

    return templates.TemplateResponse(
        request=request,
        name="politica_privacidade.html",
        context={},
    )


@app.get("/ocorrencias", response_class=HTMLResponse)
def pagina_ocorrencias(
    request: Request,
    busca: str = "",
    tipo: str = "",
):
    """Exibe e permite pesquisar os registros ambientais."""

    inicializar_banco()

    busca = busca.strip()

    conexao = obter_conexao()

    try:
        consulta = """
            SELECT
                id,
                tipo_ocorrencia,
                descricao,
                local,
                data_registro,
                latitude,
                longitude,
                precisao_metros,
                data_captura,
                foto
            FROM ocorrencias
            WHERE 1 = 1
        """

        parametros = []

        if busca:
            consulta += """
                AND (
                    descricao LIKE ?
                    OR local LIKE ?
                    OR tipo_ocorrencia LIKE ?
                )
            """

            termo = f"%{busca}%"
            parametros.extend([termo, termo, termo])

        tipos_permitidos = {
            "descarte_irregular",
            "possivel_esgoto",
            "alteracao_agua",
            "outro",
        }

        if tipo in tipos_permitidos:
            consulta += " AND tipo_ocorrencia = ?"
            parametros.append(tipo)
        else:
            tipo = ""

        consulta += " ORDER BY id DESC"

        ocorrencias = conexao.execute(
            consulta,
            parametros,
        ).fetchall()

        total_registros = conexao.execute(
            "SELECT COUNT(*) FROM ocorrencias"
        ).fetchone()[0]

    finally:
        conexao.close()

    return templates.TemplateResponse(
        request=request,
        name="ocorrencias.html",
        context={
            "ocorrencias": ocorrencias,
            "busca": busca,
            "tipo_selecionado": tipo,
            "total_registros": total_registros,
            "total_encontrado": len(ocorrencias),
        },
    )


@app.post("/ocorrencias")
def registrar_ocorrencia(
    tipo_ocorrencia: str = Form(...),
    descricao: str = Form(...),
    local: str = Form(...),
    latitude: str = Form(default=""),
    longitude: str = Form(default=""),
    precisao_metros: str = Form(default=""),
    data_captura: str = Form(default=""),
    foto: UploadFile = File(...),
):
    """Valida e registra uma ocorrência ambiental."""

    tipos_permitidos = {
        "descarte_irregular",
        "possivel_esgoto",
        "alteracao_agua",
        "outro",
    }

    if tipo_ocorrencia not in tipos_permitidos:
        return HTMLResponse(
            "Tipo de ocorrência inválido.",
            status_code=400,
        )

    descricao = descricao.strip()
    local = local.strip()

    if not descricao or not local:
        return HTMLResponse(
            "Preencha a descrição e o local da ocorrência.",
            status_code=400,
        )

    # Validação da fotografia
    if foto is None or not foto.filename:
        return HTMLResponse(
            "Envie uma fotografia da ocorrência.",
            status_code=400,
        )

    limite_foto = 5 * 1024 * 1024
    conteudo_foto = foto.file.read(limite_foto + 1)

    if len(conteudo_foto) > limite_foto:
        return HTMLResponse(
            "A fotografia deve ter no máximo 5 MB.",
            status_code=400,
        )

    try:
        imagem = Image.open(BytesIO(conteudo_foto))
        formato_foto = imagem.format
        imagem.verify()

        if formato_foto not in {"JPEG", "PNG", "WEBP"}:
            raise ValueError("Formato de imagem não permitido.")

    except (
        ValueError,
        OSError,
        SyntaxError,
        Image.DecompressionBombError,
    ):
        return HTMLResponse(
            "Arquivo inválido. Envie uma imagem JPEG, PNG ou WebP.",
            status_code=400,
        )

    # Valores iniciais da localização
    latitude_valor = None
    longitude_valor = None
    precisao_valor = None
    data_captura_valor = None

    # A localização é opcional
    if latitude.strip() or longitude.strip():
        try:
            latitude_valor = float(latitude)
            longitude_valor = float(longitude)

            if not math.isfinite(latitude_valor):
                raise ValueError

            if not math.isfinite(longitude_valor):
                raise ValueError

            if not (-90 <= latitude_valor <= 90):
                raise ValueError

            if not (-180 <= longitude_valor <= 180):
                raise ValueError

        except (ValueError, TypeError):
            return HTMLResponse(
                "As coordenadas informadas são inválidas.",
                status_code=400,
            )

        if precisao_metros.strip():
            try:
                precisao_valor = float(precisao_metros)

                if not math.isfinite(precisao_valor):
                    raise ValueError

                if precisao_valor < 0:
                    raise ValueError

            except (ValueError, TypeError):
                return HTMLResponse(
                    "O valor da precisão do GPS é inválido.",
                    status_code=400,
                )

        if data_captura.strip():
            data_captura_valor = data_captura.strip()

    # Preparação do caminho da fotografia
    PASTA_FOTOS.mkdir(parents=True, exist_ok=True)

    extensoes_foto = {
        "JPEG": ".jpg",
        "PNG": ".png",
        "WEBP": ".webp",
    }

    nome_arquivo_foto = (
        f"{uuid4().hex}{extensoes_foto[formato_foto]}"
    )

    caminho_foto = PASTA_FOTOS / nome_arquivo_foto
    caminho_foto_relativo = f"/static/fotos/{nome_arquivo_foto}"

    data_registro = datetime.now(timezone.utc).isoformat(
        timespec="seconds"
    )

    conexao = obter_conexao()

    try:
        caminho_foto.write_bytes(conteudo_foto)

        conexao.execute(
            """
            INSERT INTO ocorrencias (
                tipo_ocorrencia,
                descricao,
                local,
                data_registro,
                latitude,
                longitude,
                precisao_metros,
                data_captura,
                foto
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                tipo_ocorrencia,
                descricao,
                local,
                data_registro,
                latitude_valor,
                longitude_valor,
                precisao_valor,
                data_captura_valor,
                caminho_foto_relativo,
            ),
        )

        conexao.commit()

    except Exception:
        try:
            conexao.rollback()
        except Exception:
            pass

        try:
            if caminho_foto.exists():
                caminho_foto.unlink()
        except OSError:
            pass

        raise

    finally:
        conexao.close()
        foto.file.close()

    return RedirectResponse(
        url="/?sucesso=1",
        status_code=303,
    )


@app.post("/comentarios")
def registrar_comentario(
    nome: str = Form(default=""),
    mensagem: str = Form(...),
):
    """Valida e registra um comentário da comunidade."""

    nome = nome.strip()
    mensagem = mensagem.strip()

    # O nome é opcional, mas possui limite de tamanho.
    if len(nome) > 60:
        return HTMLResponse(
            "O nome deve ter no máximo 60 caracteres.",
            status_code=400,
        )

    # A mensagem é obrigatória.
    if not mensagem:
        return HTMLResponse(
            "Digite uma mensagem antes de enviar.",
            status_code=400,
        )

    # Limita o tamanho da mensagem.
    if len(mensagem) > 1000:
        return HTMLResponse(
            "A mensagem deve ter no máximo 1.000 caracteres.",
            status_code=400,
        )

    data_registro = datetime.now(timezone.utc).isoformat(
        timespec="seconds"
    )

    conexao = obter_conexao()

    try:
        conexao.execute(
            """
            INSERT INTO comentarios (
                nome,
                mensagem,
                data_registro
            )
            VALUES (?, ?, ?)
            """,
            (
                nome or None,
                mensagem,
                data_registro,
            ),
        )

        conexao.commit()

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()

    return RedirectResponse(
        url="/?comentario=1#comentarios",
        status_code=303,
    )