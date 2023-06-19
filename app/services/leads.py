from datetime import datetime
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.models import DBLead
from app.models.schemas import LeadPayload, LeadResponse, UserResponse
from app.config import get_settings
from sqlalchemy.orm import Query


settings = get_settings()

key = settings.secret_key
algorithm = settings.algorithm


async def create_lead(payload: LeadPayload, user: UserResponse, db: Session) -> LeadResponse:
    db_lead: DBLead = DBLead(**payload.dict(), owner_id=user.id)
    db.add(instance=db_lead)
    db.commit()
    db.refresh(instance=db_lead)
    return LeadResponse.from_orm(obj=db_lead)


async def get_leads(user: UserResponse, db: Session) -> List[LeadResponse]:
    db_leads: Query[DBLead] = db.query(DBLead).filter_by(owner_id=user.id)

    return list(map(LeadResponse.from_orm, db_leads))


async def lead_selector(lead_id: int, user: UserResponse, db: Session) -> DBLead:
    db_lead: DBLead = (
        db.query(DBLead)
        .filter_by(owner_id=user.id)
        .filter(DBLead.id == lead_id)
        .first()
    )

    if db_lead is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Lead with id [{lead_id}] does not exist")

    return db_lead


async def get_lead(lead_id: int, user: UserResponse, db: Session) -> LeadResponse:
    db_lead: DBLead = await lead_selector(lead_id=lead_id, user=user, db=db)

    return LeadResponse.from_orm(obj=db_lead)


async def delete_lead(lead_id: int, user: UserResponse, db: Session) -> None:
    db_lead: DBLead = await lead_selector(lead_id=lead_id, user=user, db=db)

    db.delete(instance=db_lead)
    db.commit()


async def update_lead(
    lead_id: int, payload: LeadPayload, user: UserResponse, db: Session
) -> LeadResponse:
    db_lead: DBLead = await lead_selector(lead_id=lead_id, user=user, db=db)

    for key, value in payload.dict().items():
        setattr(db_lead, key, value)
    db_lead.date_updated = datetime.utcnow()

    db.commit()
    db.refresh(instance=db_lead)

    return LeadResponse.from_orm(obj=db_lead)
