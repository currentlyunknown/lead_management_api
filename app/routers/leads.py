from typing import Any, Dict, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.models.schemas import LeadPayload, LeadResponse, UserResponse
from app.services.database import get_db
from app.services.leads import (
    create_lead,
    delete_lead,
    get_lead,
    get_leads,
    update_lead,
)
from app.services.users import get_current_user

router = APIRouter(prefix="/api/leads")


@router.post("", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
async def api_create_lead(
    payload: LeadPayload,
    user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    return await create_lead(payload=payload, user=user, db=db)


@router.get("", response_model=List[LeadResponse])
async def api_get_leads(
    user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[Dict[str, Any]]:
    return await get_leads(user=user, db=db)


@router.get("/{lead_id}", response_model=LeadResponse)
async def api_get_lead(
    lead_id: int,
    user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    return await get_lead(lead_id=lead_id, user=user, db=db)


@router.delete("/{lead_id}", status_code=status.HTTP_204_NO_CONTENT)
async def api_delete_lead(
    lead_id: int,
    user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    await delete_lead(lead_id=lead_id, user=user, db=db)


@router.put("/{lead_id}")
async def api_update_lead(
    lead_id: int,
    payload: LeadPayload,
    user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    return await update_lead(lead_id=lead_id, payload=payload, user=user, db=db)
