from fastapi import APIRouter, HTTPException
from app.models import Assistant, AssistantDB
from typing import Optional

router = APIRouter()


@router.post("/assistants", response_model=Assistant, summary="Create an assistant",
             description="Create a new assistant with a unique ID.",
             response_description="The created assistant.",
             tags=["Assistants"])
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
            tags=["Assistants"])
async def get_assistant(assistant_id: str):
    assistant = await AssistantDB.get(assistant_id)
    if not assistant:
        raise HTTPException(status_code=404, detail="Assistant not found")
    return assistant
