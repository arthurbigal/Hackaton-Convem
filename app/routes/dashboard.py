"""Rota do dashboard resumido de incidentes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas.incident import DashboardResponse
from app.services import incident_service

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db)):
    return incident_service.get_dashboard_summary(db)