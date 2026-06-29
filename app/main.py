# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.clients.http import init_client, close_client
from app.routers.audit import router as audit_router
from app.routers.pages import router as pages_router
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Выполняется при старте (аналог Django signals post_migrate или ready())
    await init_client()
    yield
    # Выполняется при остановке
    await close_client()


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(audit_router)
app.include_router(pages_router)
