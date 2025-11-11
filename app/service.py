from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository import IncidentRepository
from app.schemas import IncidentCreate, IncidentUpdate

class IncidentService:
    def __init__(self, db: AsyncSession):
        self.repository = IncidentRepository(db)

    async def create_incident(self, incident: IncidentCreate):
        return await self.repository.create_incident(
            description=incident.description,
            source=incident.source
        )

    async def get_incidents(
        self,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ):
        return await self.repository.get_incidents(
            status=status,
            skip=skip,
            limit=limit
        )

    async def update_incident_status(
        self,
        incident_id: int,
        incident_update: IncidentUpdate
    ):
        return await self.repository.update_incident_status(
            incident_id=incident_id,
            status=incident_update.status
        )