from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db
from app.schemas import Incident, IncidentCreate, IncidentUpdate
from app.service import IncidentService

router = APIRouter()

@router.post("/", response_model=Incident, status_code=status.HTTP_201_CREATED)
async def create_incident(
    incident: IncidentCreate,
    db: AsyncSession = Depends(get_db)
):
    service = IncidentService(db)
    return await service.create_incident(incident)

@router.get("/", response_model=list[Incident])
async def read_incidents(
    status: Optional[str] = Query(None, description="Filter by status"),
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    service = IncidentService(db)
    return await service.get_incidents(status=status, skip=skip, limit=limit)

@router.patch("/{incident_id}/status", response_model=Incident)
async def update_incident_status(
    incident_id: int,
    incident_update: IncidentUpdate,
    db: AsyncSession = Depends(get_db)
):
    service = IncidentService(db)
    db_incident = await service.update_incident_status(
        incident_id=incident_id,
        incident_update=incident_update
    )
    if db_incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return db_incident