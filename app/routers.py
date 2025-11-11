from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas import Incident, IncidentCreate, IncidentUpdate
from app import repository

router = APIRouter()

@router.post("/", response_model=Incident, status_code=status.HTTP_201_CREATED)
def create_incident(incident: IncidentCreate, db: Session = Depends(get_db)):
    return repository.create_incident(db=db, incident=incident)

@router.get("/", response_model=list[Incident])
def read_incidents(
    status: Optional[str] = Query(None, description="Filter by status"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    incidents = repository.get_incidents(db, status=status, skip=skip, limit=limit)
    return incidents

@router.patch("/{incident_id}/status", response_model=Incident)
def update_incident_status(incident_id: int, incident_update: IncidentUpdate, db: Session = Depends(get_db)):
    db_incident = repository.update_incident_status(db, incident_id=incident_id, status=incident_update.status)
    if db_incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return db_incident