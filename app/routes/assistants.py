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
