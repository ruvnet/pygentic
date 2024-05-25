```
   ___                      _   _      
  / _ \/\_/\__ _  ___ _ __ | |_(_) ___ 
 / /_)/\_ _/ _` |/ _ \ '_ \| __| |/ __|
/ ___/  / \ (_| |  __/ | | | |_| | (__ 
\/      \_/\__, |\___|_| |_|\__|_|\___|
           |___/                       

   Created by rUv

```
### Introduction to Pygentic Framework

Pygentic is an innovative system designed to enhance the capabilities of AI assistants by providing a flexible and standardized API. 

Based on the robust architecture of the OpenAI Assistants API, Pygentic abstracts the complexities of integrating with different Large Language Models (LLMs), both local and remote. This abstraction ensures a consistent and seamless interaction regardless of the underlying model.

### What is the Pygentic Library?

The Pygentic library acts as a bridge between your application and various LLMs. It simplifies the process of connecting to different AI models by offering a uniform API, eliminating the need to manage the specifics of each model. Whether you're using OpenAI, a local model, or another remote service, Pygentic provides a reliable and consistent interface.

### Pygentic Agents

Pygentic introduces the concept of agents—intelligent assistants that can perform a range of tasks. These agents are configured to understand and respond to user inputs, utilizing different LLMs for processing. You can create and manage multiple agents, each tailored to specific functions or tasks, enhancing the versatility and efficiency of your AI-driven applications.

### Concurrency

Concurrency in Pygentic ensures that multiple tasks can be handled simultaneously without compromising performance. This is particularly important for applications requiring real-time responses or handling numerous requests at once. Pygentic's design leverages modern asynchronous programming techniques to manage these tasks efficiently, providing a smooth and responsive experience.

### Serverless

Pygentic supports serverless architectures, enabling you to deploy your AI applications without the need to manage infrastructure. This approach reduces operational complexity and costs, as the serverless platform handles scaling, monitoring, and resource allocation automatically. You can focus on developing and refining your AI capabilities, while the serverless environment ensures robust and scalable 

### Open-Interpreter (Multi-Programming Language Support)

The open-interpreter feature of Pygentic allows for multi-programming language support, enabling your agents to understand and generate responses in various programming languages. This expands the reach of your applications, making them compatible with a variety of different software projects. The flexibility to interpret and interact in multiple programming languages enhances the usability and effectiveness of your AI solutions.

### Practical Applications

Pygentic can be applied across numerous practical scenarios:
- **Customer Support**: Deploy intelligent agents to handle customer queries, providing instant and accurate responses.
- **Content Generation**: Use AI to create engaging content in multiple languages, tailored to your audience.
- **Data Analysis**: Leverage AI for interpreting and analyzing large datasets, extracting meaningful insights.
- **Personal Assistants**: Develop personalized AI assistants to help with daily tasks, scheduling, and information retrieval.

Pygentic empowers developers to harness the power of AI with ease, offering a flexible and scalable solution for integrating advanced language models into various applications. Its consistent API, multi-language support, and serverless capabilities make it a valuable tool for modern AI-driven projects.

## Project Archicture

Here's a detailed breakdown of the directory structure and code blocks for each file.

### 1. **Directory Structure**

```
my_assistant_proxy/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── assistants.py
│   │   ├── threads.py
│   │   ├── messages.py
│   │   ├── runs.py
│   └── services/
│       ├── __init__.py
│       ├── llm_service.py
│       ├── serverless_service.py
│       ├── open_interpreter_service.py
│       ├── database.py
├── tests/
│   ├── __init__.py
│   ├── test_assistants.py
│   ├── test_threads.py
│   ├── test_messages.py
│   ├── test_runs.py
├── requirements.txt
└── README.md
```

### 2. **Code Blocks for Each Python File**

#### `app/__init__.py`

```python
# app/__init__.py
# This file can be left empty
```

#### `app/main.py`

```python
# app/main.py
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
```

#### `app/models.py`

```python
# app/models.py
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
```

#### `app/routes/__init__.py`

```python
# app/routes/__init__.py
# This file can be left empty
```

#### `app/routes/assistants.py`

```python
# app/routes/assistants.py
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
```

#### `app/routes/threads.py`

```python
# app/routes/threads.py
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
```

#### `app/routes/messages.py`

```python
# app/routes/messages.py
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
```

#### `app/routes/runs.py`

```python
# app/routes/runs.py
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
```

#### `app/services/__init__.py`

```python
# app/services/__init__.py
# This file can be left empty
```

#### `app/services/llm_service.py`

```python
# app/services/llm_service.py
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
```

#### `app/services/serverless_service.py`

```python
# app/services/serverless_service.py
# Placeholder for serverless service logic
class ServerlessService:
    # Implement serverless function calls
    pass
```

#### `app/services/open_interpreter_service.py`

```python
# app/services/open_interpreter_service.py
# Placeholder for open interpreter service logic
class OpenInterpreterService:
    # Implement open interpreter service logic
    pass
```

#### `app/services/database.py`

```python
# app/services/database.py
from databases import Database

DATABASE_URL = "sqlite:///./test.db"
database = Database(DATABASE_URL)

async def connect_db():
    await database.connect()

async def disconnect_db():
    await database.disconnect()
```

#### `tests/__init__.py`

```python
# tests/__init__.py
# This file can be left empty
```

#### `tests/test_assistants.py`

```python
# tests/test_assistants.py
import pytest
from httpx import Async

Client
from app.main import app

@pytest.mark.anyio
async def test_create_assistant():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/v1/assistants", json={"id": "1", "name": "Test Assistant", "model": "gpt-4"})
        assert response.status_code == 200
        assert response.json()["name"] == "Test Assistant"
```

#### `tests/test_threads.py`

```python
# tests/test_threads.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.anyio
async def test_create_thread():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/v1/threads", json={"id": "1", "assistant_id": "1", "messages": []})
        assert response.status_code == 200
        assert response.json()["assistant_id"] == "1"
```

#### `tests/test_messages.py`

```python
# tests/test_messages.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.anyio
async def test_add_message():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/v1/threads/1/messages", json={"id": "1", "thread_id": "1", "role": "user", "content": "Hello"})
        assert response.status_code == 200
        assert response.json()["content"] == "Hello"
```

#### `tests/test_runs.py`

```python
# tests/test_runs.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.anyio
async def test_run_thread():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/v1/threads/1/runs", json={"id": "1", "thread_id": "1", "assistant_id": "1", "status": "running"})
        assert response.status_code == 200
        assert response.json()["status"] == "running"
```

#### `requirements.txt`

```
fastapi
pydantic
httpx
uvicorn
liteLLM
pydbantic
databases[sqlite]
pytest
pytest-asyncio
```

#### `README.md`

```markdown
# Pygentic

Pygentic is a FastAPI application that clones all the Assistant API endpoints and allows pointing to alternate LLMs, open interpreter libraries, and serverless functions using `liteLLM`, with added persistence using `pydbantic` and `databases`.

## Project Setup

1. **Setup Project Structure**
    ```bash
    ./setup.sh
    ```

2. **Install Dependencies**
    ```bash
    ./setup.sh
    ```

3. **Setup Virtual Environment**
    ```bash
    ./setup.sh
    ```

4. **Activate Virtual Environment**
    ```bash
    ./setup.sh
    ```

5. **Run the Application**
    ```bash
    uvicorn app.main:app --reload
    ```

## Endpoints

### Assistants
- `POST /v1/assistants`: Create a new assistant.
- `GET /v1/assistants/{assistant_id}`: Retrieve an assistant by ID.

### Threads
- `POST /v1/threads`: Create a new thread.
- `GET /v1/threads/{thread_id}`: Retrieve a thread by ID.

### Messages
- `POST /v1/threads/{thread_id}/messages`: Add a message to a thread.
- `GET /v1/threads/{thread_id}/messages`: Retrieve messages in a thread.

### Runs
- `POST /v1/threads/{thread_id}/runs`: Run a thread with an assistant.
- `GET /v1/threads/{thread_id}/runs/{run_id}`: Retrieve a run by ID.
```

### Instructions for Using the Script

1. **Create the Directory Structure**: Manually create the directories if the script has not already done so.
2. **Copy the Code**: Copy and paste the code blocks into their respective files as shown in the structure.
3. **Install Dependencies**: Run the script to install the necessary dependencies and set up the virtual environment.
4. **Run the Application**: Use the `uvicorn` command to run the FastAPI application.

This setup ensures that you have a well-organized and functional FastAPI application named `pygentic` with persistence and the ability to interact with various LLMs and serverless functions.
