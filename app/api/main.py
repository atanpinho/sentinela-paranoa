from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
PASTA_PROJETO = Path(__file__).resolve().parents[2]
PASTA_TEMPLATES = PASTA_PROJETO / "app" / "templates"
PASTA_STATIC = PASTA_PROJETO / "app" / "static"
templates = Jinja2Templates(directory=str(PASTA_TEMPLATES))

app.mount(
    "/static",
    StaticFiles(directory=str(PASTA_STATIC)),
    name="static",
)

@app.get("/", response_class=HTMLResponse)
async def pagina_inicial(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"alerts": []},
    )
