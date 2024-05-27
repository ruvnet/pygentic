import sys
from pathlib import Path
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.responses import RedirectResponse
from app.routes import assistants, threads, messages, runs
from app.services.database import connect_db, disconnect_db
from app.services.connector import DatabaseConnector, LLMServiceConnector
from app import config

# Add the root directory and app directory to the PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))
sys.path.append(str(Path(__file__).resolve().parent))

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await disconnect_db()

app = FastAPI(
    title="Pygentic",
    description="Pygentic API documentation",
    version="0.1.0",
    lifespan=lifespan
)

# Automatic redirect to /docs
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

app.include_router(assistants.router, prefix="/v1")
app.include_router(threads.router, prefix="/v1")
app.include_router(messages.router, prefix="/v1")
app.include_router(runs.router, prefix="/v1")

database_connector = DatabaseConnector(config["connectors"]["database"])
llm_service_connector = LLMServiceConnector(config["connectors"]["llm_service"])

@app.middleware("http")
async def add_connector_to_request(request: Request, call_next):
    request.state.db = database_connector.get_engine()
    request.state.llm_service = llm_service_connector
    response = await call_next(request)
    return response

@app.get("/generate_text")
async def generate_text(prompt: str, request: Request):
    text = request.state.llm_service.generate_text(prompt)
    return {"generated_text": text}

def run():
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    run()
