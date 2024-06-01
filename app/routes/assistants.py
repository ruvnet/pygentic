from fastapi import APIRouter, HTTPException
from app.models import Assistant, AssistantDB
from typing import Optional

router = APIRouter()


@router.post("/assistants", response_model=Assistant, summary="Create an assistant",
             description="Create a new assistant with a unique ID.",
             response_description="The created assistant.",
             tags=["Assistants"],
             examples={
                 "normal": {
                     "summary": "A normal example",
                     "description": "A **normal** assistant creation example",
                     "value": {
                         "id": "unique_id_123",
                         "name": "Assistant Name",
                         "description": "A description of the assistant",
                         "model": "gpt-3",
                         "instructions": "Some instructions",
                         "tools": ["tool1", "tool2"]
                     }
                 },
                 "test": {
                     "summary": "Test example",
                     "description": "A **test** assistant creation example",
                     "value": {
                         "id": "test_id_456",
                         "name": "Test Assistant",
                         "description": "A test description",
                         "model": "gpt-3",
                         "instructions": "Test instructions",
                         "tools": ["test_tool1", "test_tool2"]
                     }
                 }
             })
async def create_assistant(assistant: Assistant):
    assistant_db = AssistantDB(**assistant.dict())
    try:
        await assistant_db.save()
    except AttributeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return assistant


@router.get("/assistants/{assistant_id}", response_model=Assistant, summary="Get an assistant",
            description="Retrieve an assistant by its unique ID.",
            response_description="The requested assistant.",
            tags=["Assistants"],
            examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** assistant retrieval example",
                    "value": {
                        "id": "unique_id_123"
                    }
                },
                "test": {
                    "summary": "Test example",
                    "description": "A **test** assistant retrieval example",
                    "value": {
                        "id": "test_id_456"
                    }
                }
            })
async def get_assistant(assistant_id: str):
    assistant = await AssistantDB.get(assistant_id)
    if not assistant:
        raise HTTPException(status_code=404, detail="Assistant not found")
    return assistant
