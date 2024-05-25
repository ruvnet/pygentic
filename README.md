# Pygentic

Pygentic is a FastAPI application that clones all the Assistant API endpoints and allows pointing to alternate LLMs, open interpreter libraries, and serverless functions using `liteLLM`, with added persistence using `pydbantic` and `databases`.

## Project Setup

1. **Setup Project Structure**
    ```bash
    ./setup.sh
    ```

2. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Setup Virtual Environment**
    ```bash
    python -m venv venv
    ```

4. **Activate Virtual Environment**
    ```bash
    source venv/bin/activate
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
