from typing import Optional, List
from sqlalchemy.orm import Session
from app.models import Incident, IncidentStatus, IncidentSource
from app.schemas import IncidentCreate, IncidentUpdate

def create_incident(db: Session, incident: IncidentCreate):
    db_incident = Incident(
        description=incident.description,
        source=IncidentSource(incident.source)
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident

def get_incidents(db: Session, status: Optional[str] = None, skip: int = 0, limit: int = 20) -> List[Incident]:
    query = db.query(Incident)
    if status:
        query = query.filter(Incident.status == IncidentStatus(status))
    return query.offset(skip).limit(limit).all()

def update_incident_status(db: Session, incident_id: int, status: str) -> Optional[Incident]:
    db_incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if db_incident:
        db_incident.status = IncidentStatus(status)
        db.commit()
        db.refresh(db_incident)
    return db_incident