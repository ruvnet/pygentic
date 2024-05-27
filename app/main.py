import sys
import os
from pathlib import Path
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.responses import RedirectResponse
from app.routes import assistants, threads, messages, runs
from app.services.database import connect_db, disconnect_db
from app.services.plugin_loader import load_plugins
from app.services.default_connector import OpenAIAssistantConnector
from app import config
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Add the root directory and app directory to the PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))
sys.path.append(str(Path(__file__).resolve().parent))

# Load custom plugin directory from environment variable or default location
plugin_dir = os.getenv('PYGENTIC_PLUGIN_DIR', 'custom_connectors')

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

# Load plugins if the directory exists
connector_instances = {}
if os.path.isdir(plugin_dir):
    connectors = load_plugins(plugin_dir)
    for connector_class in connectors:
        connector_name = connector_class.__name__
        connector_instance = connector_class()
        connector_instance.initialize(config["connectors"].get(connector_name.lower(), {}))
        connector_instances[connector_name] = connector_instance
else:
    # Use the default OpenAIAssistantConnector if no custom plugins are available
    default_connector = OpenAIAssistantConnector()
    default_connector.initialize(config["connectors"].get("openai_assistant", {}))
    connector_instances['openaiassistantconnector'] = default_connector

@app.middleware("http")
async def add_connector_to_request(request: Request, call_next):
    for name, instance in connector_instances.items():
        setattr(request.state, name.lower(), instance)
    response = await call_next(request)
    return response

@app.get("/generate_text")
async def generate_text(prompt: str, request: Request):
    if 'openaiassistantconnector' in request.state:
        text = await request.state.openaiassistantconnector.generate_text(prompt)
        return {"generated_text": text}
    else:
        return {"error": "LLM Service Connector not available"}

def run():
    import uvicorn
    print(Fore.CYAN + Style.BRIGHT + """
       ___                      _   _      
      / _ \/\_/\__ _  ___ _ __ | |_(_) ___ 
     / /_)/\_ _/ _` |/ _ \ '_ \| __| |/ __|
    / ___/  / \ (_| |  __/ | | | |_| | (__ 
    \/      \_/\__, |\___|_| |_|\__|_|\___|
               |___/                       

        Created by rUv
    """ + Style.RESET_ALL)

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    run()
