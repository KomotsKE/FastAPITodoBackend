from typing import Optional
from pydantic import BaseModel


from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskOut(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    completed: bool

    class Config:
        from_attributes = True