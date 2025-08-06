import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .generate_token import generate_secure_link
# Modelos y acceso a BDD
from .models import SecureLink
from .crud import create_secure_link, get_secure_link, get_db


from datetime import datetime, timedelta

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "../static")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

templates_dir = os.path.join(BASE_DIR, "../templates")
templates = Jinja2Templates(directory=templates_dir)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, token: str = None):
    link = None
    if token:
        # Construir el enlace para mostrarlo en el input
        scheme = request.url.scheme
        host = request.url.hostname
        port = request.url.port
        link = f"{scheme}://{host}:{port}/secure/{token}"
    return templates.TemplateResponse("index.html", {"request": request, "link": link})


@app.post("/")
async def obtain_form(
    request: Request,
    content: str = Form(...),
    days: int = Form(...),
    visualizations: int = Form(...)
):
    # Generar token y calcular expiración
    token, _ = generate_secure_link(request)
    expires_at = datetime.utcnow() + timedelta(days=int(days))
    # Guardar en la base de datos
    db = next(get_db())
    create_secure_link(db, token, content, days, visualizations, expires_at)
    # Redirigir a GET con el token
    return RedirectResponse(url=f"/?token={token}", status_code=303)



@app.get("/secure/{token}", response_class=HTMLResponse)
async def secure(request: Request, token: str):
    db = next(get_db())
    link_data = get_secure_link(db, token)
    content = None
    expired = False
    if link_data:
        # Comprobar expiración por fecha o visualizaciones
        if link_data.is_expired():
            expired = True
        else:
            content = link_data.content
            link_data.decrement_visualizations(db)
    return templates.TemplateResponse(
        "preview.html",
        {"request": request, "content": content, "expired": expired, "token": token}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)