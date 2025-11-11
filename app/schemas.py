from pydantic import BaseModel, ConfigDict
from datetime import datetime

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

    model_config = ConfigDict(from_attributes=True)