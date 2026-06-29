# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.clients.http import init_client, close_client
from app.routers.audit import router as audit_router
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
app.include_router(audit_router)
