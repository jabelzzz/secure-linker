import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .generate_token import generate_secure_link

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "../static")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

templates_dir = os.path.join(BASE_DIR, "../templates")
templates = Jinja2Templates(directory=templates_dir)
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def obtain_form(
    request: Request,
    content: str = Form(...),
    days: int = Form(...),
    visualizations: int = Form(...)
):
    # Genera el token y el enlace usando la función separada
    token, link = generate_secure_link(request)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "content": content,
            "days": days,
            "visualizations": visualizations,
            "link": link,
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)