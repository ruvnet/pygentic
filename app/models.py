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

    class Config:
        schema_extra = {
            "example": {
                "id": "assistant_1",
                "name": "Assistant One",
                "description": "An example assistant.",
                "model": "gpt-3",
                "instructions": "Provide detailed instructions.",
                "tools": ["tool1", "tool2"]
            }
        }


class AssistantDB(DataBaseModel):
    id: str = PrimaryKey()
    name: str
    description: Optional[str] = None
    model: str
    instructions: Optional[str] = None
    tools: List[str] = []

    class Config:
        schema_extra = {
            "example": {
                "id": "assistant_db_1",
                "name": "AssistantDB One",
                "description": "An example AssistantDB.",
                "model": "gpt-3",
                "instructions": "Provide detailed instructions for AssistantDB.",
                "tools": ["tool1", "tool2"]
            }
        }


class Thread(BaseModel):
    id: str
    assistant_id: str
    messages: List[str] = []

    class Config:
        schema_extra = {
            "example": {
                "id": "thread_1",
                "assistant_id": "assistant_1",
                "messages": ["message1", "message2"]
            }
        }


class ThreadDB(DataBaseModel):
    id: str = PrimaryKey()
    assistant_id: str
    messages: List[str] = []

    class Config:
        schema_extra = {
            "example": {
                "id": "thread_db_1",
                "assistant_id": "assistant_db_1",
                "messages": ["message_db1", "message_db2"]
            }
        }


class Message(BaseModel):
    id: str
    thread_id: str
    role: str
    content: str

    class Config:
        schema_extra = {
            "example": {
                "id": "message_1",
                "thread_id": "thread_1",
                "role": "user",
                "content": "Example message content."
            }
        }


class MessageDB(DataBaseModel):
    id: str = PrimaryKey()
    thread_id: str
    role: str
    content: str

    class Config:
        schema_extra = {
            "example": {
                "id": "message_db_1",
                "thread_id": "thread_db_1",
                "role": "user",
                "content": "Example message content for MessageDB."
            }
        }


class Run(BaseModel):
    id: str
    thread_id: str
    assistant_id: str
    status: str
    result: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "id": "run_1",
                "thread_id": "thread_1",
                "assistant_id": "assistant_1",
                "status": "completed",
                "result": "Example result."
            }
        }


class RunDB(DataBaseModel):
    id: str = PrimaryKey()
    thread_id: str
    assistant_id: str
    status: str
    result: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "id": "run_db_1",
                "thread_id": "thread_db_1",
                "assistant_id": "assistant_db_1",
                "status": "completed",
                "result": "Example result for RunDB."
            }
        }
