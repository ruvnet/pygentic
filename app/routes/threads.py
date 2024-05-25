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
