from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class TaskBase(SQLModel):
    title: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    is_completed: bool = Field(default=False)

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    is_completed: Optional[bool] = Field(default=None)

class TaskOut(TaskBase):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True