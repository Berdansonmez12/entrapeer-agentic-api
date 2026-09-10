from fastapi import FastAPI

app = FastAPI(
    title="Entrapeer Agentic API",
    description="Peer-agent controlled agentic API for business discovery and problem structuring.",
    version="1.0.0",
)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "entrapeer-agentic-api",
    }