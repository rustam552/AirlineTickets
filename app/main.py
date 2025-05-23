from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routers import auth, flights
from app.database import engine
from app.models import user, ticket
from app.forms import SearchForm

app = FastAPI(title="Ticket Platform")
templates = Jinja2Templates(directory="app/templates")

# Создание таблиц
user.Base.metadata.create_all(bind=engine)
ticket.Base.metadata.create_all(bind=engine)

# Роутеры подключающие маршруты
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(flights.router, prefix="/flights", tags=["flights"])

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    form = SearchForm()
    return templates.TemplateResponse("search.html", {"request": request, "form": form})