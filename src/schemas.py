from pydantic import BaseModel
from typing import List, Optional
from pydantic import ConfigDict

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    status: str
    owner_id: int
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: str
    password: str

class User(BaseModel):
    id: int
    email: str
    tasks: List[Task] = []
    model_config = ConfigDict(from_attributes=True)