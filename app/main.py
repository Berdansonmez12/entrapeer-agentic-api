from fastapi import FastAPI

from app.api.routes import router as agent_router


app = FastAPI(
    title="Entrapeer Agentic API",
    description="Peer-agent controlled agentic API for business discovery and problem structuring.",
    version="1.0.0",
)

app.include_router(agent_router)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "entrapeer-agentic-api",
    }