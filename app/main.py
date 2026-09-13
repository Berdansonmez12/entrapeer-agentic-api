from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router as agent_router
from app.db.mongo import mongodb


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await mongodb.connect()
        print("MongoDB connected.")
    except Exception as exc:
        print(f"[STARTUP WARNING] MongoDB unavailable: {exc}")
        await mongodb.disconnect()

    yield

    await mongodb.disconnect()


app = FastAPI(
    title="Entrapeer Agentic API",
    description="Peer-agent controlled agentic API for business discovery and problem structuring.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(agent_router)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "entrapeer-agentic-api",
    }