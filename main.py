import sys
from pathlib import Path

# Add the app directory to the PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent / "app"))

from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import assistants, threads, messages, runs
from services.database import connect_db, disconnect_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await disconnect_db()

app = FastAPI(
    title="Pygentic",
    lifespan=lifespan
)

app.include_router(assistants.router, prefix="/v1")
app.include_router(threads.router, prefix="/v1")
app.include_router(messages.router, prefix="/v1")
app.include_router(runs.router, prefix="/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
