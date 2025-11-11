from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class IncidentBase(BaseModel):
    description: str
    source: str

class IncidentCreate(IncidentBase):
    pass

class IncidentUpdate(BaseModel):
    status: str

class Incident(IncidentBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True