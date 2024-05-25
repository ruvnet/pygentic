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
