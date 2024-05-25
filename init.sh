#!/bin/bash

# Define the base directory
BASE_DIR="."

# Create directory structure
mkdir -p $BASE_DIR/app/routes
mkdir -p $BASE_DIR/app/services
mkdir -p $BASE_DIR/tests

# Create __init__.py files
touch $BASE_DIR/app/__init__.py
touch $BASE_DIR/app/routes/__init__.py
touch $BASE_DIR/app/services/__init__.py
touch $BASE_DIR/tests/__init__.py

# Create main files with content
cat <<EOL > $BASE_DIR/app/main.py
from fastapi import FastAPI
from app.routes import assistants, threads, messages, runs
from app.services.database import connect_db, disconnect_db

app = FastAPI()

app.include_router(assistants.router, prefix="/v1")
app.include_router(threads.router, prefix="/v1")
app.include_router(messages.router, prefix="/v1")
app.include_router(runs.router, prefix="/v1")

@app.on_event("startup")
async def startup():
    await connect_db()

@app.on_event("shutdown")
async def shutdown():
    await disconnect_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOL

cat <<EOL > $BASE_DIR/app/models.py
from pydantic import BaseModel
from pydbantic import DataBaseModel, PrimaryKey
from typing import List, Optional

class Assistant(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    model: str
    instructions: Optional[str] = None
    tools: List[str] = []

class AssistantDB(DataBaseModel):
    id: str = PrimaryKey()
    name: str
    description: Optional[str] = None
    model: str
    instructions: Optional[str] = None
    tools: List[str] = []

class Thread(BaseModel):
    id: str
    assistant_id: str
    messages: List[str] = []

class ThreadDB(DataBaseModel):
    id: str = PrimaryKey()
    assistant_id: str
    messages: List[str] = []

class Message(BaseModel):
    id: str
    thread_id: str
    role: str
    content: str

class MessageDB(DataBaseModel):
    id: str = PrimaryKey()
    thread_id: str
    role: str
    content: str

class Run(BaseModel):
    id: str
    thread_id: str
    assistant_id: str
    status: str
    result: Optional[str] = None

class RunDB(DataBaseModel):
    id: str = PrimaryKey()
    thread_id: str
    assistant_id: str
    status: str
    result: Optional[str] = None
EOL

# Create routes files with content
cat <<EOL > $BASE_DIR/app/routes/assistants.py
from fastapi import APIRouter, HTTPException
from app.models import Assistant, AssistantDB

router = APIRouter()

@router.post("/assistants", response_model=Assistant)
async def create_assistant(assistant: Assistant):
    assistant_db = AssistantDB(**assistant.dict())
    await assistant_db.save()
    return assistant

@router.get("/assistants/{assistant_id}", response_model=Assistant)
async def get_assistant(assistant_id: str):
    assistant = await AssistantDB.get(assistant_id)
    if not assistant:
        raise HTTPException(status_code=404, detail="Assistant not found")
    return assistant
EOL

cat <<EOL > $BASE_DIR/app/routes/threads.py
from fastapi import APIRouter, HTTPException
from app.models import Thread, ThreadDB

router = APIRouter()

@router.post("/threads", response_model=Thread)
async def create_thread(thread: Thread):
    thread_db = ThreadDB(**thread.dict())
    await thread_db.save()
    return thread

@router.get("/threads/{thread_id}", response_model=Thread)
async def get_thread(thread_id: str):
    thread = await ThreadDB.get(thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    return thread
EOL

cat <<EOL > $BASE_DIR/app/routes/messages.py
from fastapi import APIRouter, HTTPException
from typing import List
from app.models import Message, MessageDB

router = APIRouter()

@router.post("/threads/{thread_id}/messages", response_model=Message)
async def add_message(thread_id: str, message: Message):
    message_db = MessageDB(**message.dict())
    await message_db.save()
    return message

@router.get("/threads/{thread_id}/messages", response_model=List[Message])
async def get_messages(thread_id: str):
    messages = await MessageDB.filter(thread_id=thread_id)
    return messages
EOL

cat <<EOL > $BASE_DIR/app/routes/runs.py
from fastapi import APIRouter, HTTPException
from app.models import Run, RunDB

router = APIRouter()

@router.post("/threads/{thread_id}/runs", response_model=Run)
async def run_thread(thread_id: str, run: Run):
    run_db = RunDB(**run.dict())
    await run_db.save()
    return run

@router.get("/threads/{thread_id}/runs/{run_id}", response_model=Run)
async def get_run(thread_id: str, run_id: str):
    run = await RunDB.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run
EOL

# Create services files with content
cat <<EOL > $BASE_DIR/app/services/llm_service.py
from app.models import Assistant, Thread, Message, Run
from liteLLM import LLMClient

class LLMService:
    client = LLMClient(api_key="your_api_key")

    @staticmethod
    async def create_assistant(assistant: Assistant):
        response = await LLMService.client.create_assistant(
            name=assistant.name,
            model=assistant.model,
            instructions=assistant.instructions,
            tools=assistant.tools
        )
        return response

    @staticmethod
    async def get_assistant(assistant_id: str):
        response = await LLMService.client.get_assistant(assistant_id)
        return response

    @staticmethod
    async def create_thread(thread: Thread):
        response = await LLMService.client.create_thread(
            assistant_id=thread.assistant_id,
            messages=thread.messages
        )
        return response

    @staticmethod
    async def get_thread(thread_id: str):
        response = await LLMService.client.get_thread(thread_id)
        return response

    @staticmethod
    async def add_message(thread_id: str, message: Message):
        response = await LLMService.client.add_message(
            thread_id=thread_id,
            role=message.role,
            content=message.content
        )
        return response

    @staticmethod
    async def get_messages(thread_id: str):
        response = await LLMService.client.get_messages(thread_id)
        return response

    @staticmethod
    async def run_thread(thread_id: str, run: Run):
        response = await LLMService.client.run_thread(
            thread_id=thread_id,
            assistant_id=run.assistant_id
        )
        return response

    @staticmethod
    async def get_run(thread_id: str, run_id: str):
        response = await LLMService.client.get_run(thread_id, run_id)
        return response
EOL

cat <<EOL > $BASE_DIR/app/services/serverless_service.py
# Placeholder for serverless service logic
class ServerlessService:
    # Implement serverless function calls
    pass
EOL

cat <<EOL > $BASE_DIR/app/services/open_interpreter_service.py
# Placeholder for open interpreter service logic
class OpenInterpreterService:
    # Implement open interpreter service logic
    pass
EOL

cat <<EOL > $BASE_DIR/app/services/database.py
from databases import Database

DATABASE_URL = "sqlite:///./test.db"
database = Database(DATABASE_URL)

async def connect_db():
    await database.connect()

async def disconnect_db():
    await database.disconnect()
EOL

# Create test files with content
cat <<EOL > $BASE_DIR/tests/test_assistants.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.anyio
async def test_create_assistant():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/v1/assistants", json={"id": "1", "name": "Test Assistant", "model": "gpt-4"})
        assert response.status_code == 200
        assert response.json()["name"] == "Test Assistant"
EOL

cat <<EOL > $BASE_DIR/tests/test_threads.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.anyio
async def test_create_thread():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/v1/threads", json={"id": "1", "assistant_id": "1", "messages": []})
        assert response.status_code == 200
        assert response.json()["assistant_id"] == "1"
EOL

cat <<EOL > $BASE_DIR/tests/test_messages.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.anyio
async def test_add_message():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/v1/threads/1/messages", json={"id": "1", "thread_id": "1", "role": "user", "content": "Hello"})
        assert response.status_code == 200
        assert response.json()["content"] == "Hello"
EOL

cat <<EOL > $BASE_DIR/tests/test_runs.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.anyio
async def test_run_thread():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/v1/threads/1/runs", json={"id": "1", "thread_id": "1", "assistant_id": "1", "status": "running"})
        assert response.status_code == 200
        assert response.json()["status"] == "running"
EOL

# Create requirements.txt
cat <<EOL > $BASE_DIR/requirements.txt
fastapi
pydantic
httpx
uvicorn
liteLLM
pydbantic
databases[sqlite]
pytest
pytest-asyncio
EOL

# Create README.md
cat <<EOL > $BASE_DIR/README.md
# Pygentic

Pygentic is a FastAPI application that clones all the Assistant API endpoints and allows pointing to alternate LLMs, open interpreter libraries, and serverless functions using \`liteLLM\`, with added persistence using \`pydbantic\` and \`databases\`.

## Project Setup

1. **Setup Project Structure**
    \`\`\`bash
    ./setup.sh
    \`\`\`

2. **Install Dependencies**
    \`\`\`bash
    pip install -r requirements.txt
    \`\`\`

3. **Setup Virtual Environment**
    \`\`\`bash
    python -m venv venv
    \`\`\`

4. **Activate Virtual Environment**
    \`\`\`bash
    source venv/bin/activate
    \`\`\`

5. **Run the Application**
    \`\`\`bash
    uvicorn app.main:app --reload
    \`\`\`

## Endpoints

### Assistants
- \`POST /v1/assistants\`: Create a new assistant.
- \`GET /v1/assistants/{assistant_id}\`: Retrieve an assistant by ID.

### Threads
- \`POST /v1/threads\`: Create a new thread.
- \`GET /v1/threads/{thread_id}\`: Retrieve a thread by ID.

### Messages
- \`POST /v1/threads/{thread_id}/messages\`: Add a message to a thread.
- \`GET /v1/threads/{thread_id}/messages\`: Retrieve messages in a thread.

### Runs
- \`POST /v1/threads/{thread_id}/runs\`: Run a thread with an assistant.
- \`GET /v1/threads/{thread_id}/runs/{run_id}\`: Retrieve a run by ID.
EOL

echo "Project setup script completed successfully."
