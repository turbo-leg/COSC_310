"""
Controller for admin-specific endpoints.
"""

from fastapi import APIRouter, HTTPException
from app.services.admin_service import admin_service
from app.services.auth_service import auth_service
from app.schemas import AdminStatsResponse

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/stats", response_model=AdminStatsResponse)
def get_admin_stats(user_id: int):
    """
    Get system statistics. Admin only.
    """
    if not auth_service.authorize_admin(user_id):
        raise HTTPException(
            status_code=403,
            detail="Forbidden: Admin access required"
        )
    return admin_service.get_stats()
