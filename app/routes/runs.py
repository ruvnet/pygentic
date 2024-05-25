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
