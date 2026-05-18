from fastapi import APIRouter, status, HTTPException, Query
from sqlmodel import func, select
from app.models.leads import Lead, LeadBase
from db import session_dependency
from datetime import datetime
from app.services import leads as leads_service

router = APIRouter(prefix="/api", tags=["leads"])

@router.post("/leads", status_code=status.HTTP_201_CREATED)
async def create_lead(lead: LeadBase, session: session_dependency):
    lead_validated = LeadBase.model_validate(lead.model_dump())
    lead_create = Lead(**lead_validated.model_dump())
    session.add(lead_create)
    session.commit()
    session.refresh(lead_create)
    return lead_create

@router.get("/leads", status_code=status.HTTP_200_OK)
async def get_leads(session: session_dependency,
                    fuente: str = Query(None, description="Filtrar por fuente de lead"),
                    producto_interes: str = Query(None, description="Filtrar por producto de interés")):
    query = select(Lead)
    if fuente:
        query = query.where(Lead.fuente == fuente)
    if producto_interes:
        query = query.where(Lead.producto_interes == producto_interes)
    leads = session.exec(query).all()
    return leads

@router.get("/leads/{lead_id}", status_code=status.HTTP_200_OK)
async def get_lead(lead_id: str, session: session_dependency):
    lead_db = session.get(Lead, lead_id)
    if not lead_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead no encontrado")
    return lead_db

@router.patch("/leads/{lead_id}", status_code=status.HTTP_200_OK)
async def update_lead(lead_id: str, lead_data: LeadBase, session: session_dependency):
    lead_db = session.get(Lead, lead_id)
    if not lead_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead no encontrado")
    lead_validated = LeadBase.model_validate(lead_data.model_dump(exclude_unset=True))
    lead_db.sqlmodel_update(lead_validated.model_dump(exclude_unset=True))
    lead_db.updated_at = datetime.now()
    session.add(lead_db)
    session.commit()
    session.refresh(lead_db)
    return lead_db

@router.delete("/leads/{lead_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lead(lead_id: str, session: session_dependency):
    lead_db = session.get(Lead, lead_id)
    if not lead_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead no encontrado")
    session.delete(lead_db)
    session.commit()
    return None

# Endpoint de soft delete
@router.delete("/leads/{lead_id}/soft", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_lead(lead_id: str, session: session_dependency):
    lead_db = session.get(Lead, lead_id)
    if not lead_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead no encontrado")
    lead_db.deleted = True
    lead_db.updated_at = datetime.now()
    session.add(lead_db)
    session.commit()
    return None

# Endpoint para retornar estadísticas
@router.get("/leads/stats", status_code=status.HTTP_200_OK)
async def get_leads_stats(session: session_dependency):
    print("Obteniendo estadísticas de leads...")
    data = leads_service.get_leads_stats(session)
    print(f"Estadísticas obtenidas: {data}")
    return data