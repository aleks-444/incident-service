from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.models import Incident, IncidentStatus, IncidentSource


class IncidentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_incident(self, description: str, source: str) -> Incident:
        db_incident = Incident(
            description=description,
            source=IncidentSource(source)
        )
        self.db.add(db_incident)
        await self.db.commit()
        await self.db.refresh(db_incident)
        return db_incident

    async def get_incidents(
            self,
            status: Optional[str] = None,
            skip: int = 0,
            limit: int = 20
    ) -> List[Incident]:
        query = select(Incident)
        if status:
            query = query.where(Incident.status == IncidentStatus(status))

        result = await self.db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()

    async def update_incident_status(
            self,
            incident_id: int,
            status: str
    ) -> Optional[Incident]:
        result = await self.db.execute(
            select(Incident).where(Incident.id == incident_id)
        )
        db_incident = result.scalar_one_or_none()

        if db_incident:
            db_incident.status = IncidentStatus(status)
            await self.db.commit()
            await self.db.refresh(db_incident)

        return db_incident

    async def get_incident_by_id(self, incident_id: int) -> Optional[Incident]:
        result = await self.db.execute(
            select(Incident).where(Incident.id == incident_id)
        )
        return result.scalar_one_or_none()