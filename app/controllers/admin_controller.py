"""
Controller for admin-specific endpoints.
"""

from fastapi import APIRouter, HTTPException
from app.auth_helpers import require_admin
from app.services.admin_service import admin_service
from app.services.auth_service import auth_service
from app.schemas import AdminStatsResponse

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/stats", response_model=AdminStatsResponse)
def get_admin_stats(user_id: int):
    """
    Get system statistics. Admin only.
    """
    require_admin(user_id)
    return admin_service.get_stats()
