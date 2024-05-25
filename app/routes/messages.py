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
