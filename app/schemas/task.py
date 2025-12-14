from pydantic import BaseModel
from datetime import datetime


class TaskCreate(BaseModel):
    title : str
    description : str | None = None
    due_date : datetime | None = None
    priority : str

class TaskUpdate(BaseModel):
    title : str | None = None
    description : str | None = None
    due_date : datetime | None = None
    priority : str | None = None
    status : str | None = None

class TaskRead(BaseModel):
    id : int
    title : str
    description : str | None = None
    due_date : datetime | None = None
    priority : str
    status : str
    created_at : datetime
    updated_at : datetime
    owner_id : int | None = None

    class Config:
        from_attributes = True

