"""
Controller for admin-specific endpoints.
"""

from fastapi import APIRouter
from app.auth_helpers import require_admin
from app.services.admin_service import admin_service
from app.schemas import AdminStatsResponse, PromoCreateRequest

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/stats", response_model=AdminStatsResponse)
def get_admin_stats(user_id: int):
    """
    Get system statistics. Admin only.
    """
    require_admin(user_id)
    return admin_service.get_stats()

@router.post("/promo")
def create_promo(request: PromoCreateRequest, user_id: int):
    """
    Endpoint to create promo code data
    """
    require_admin(user_id)

    return admin_service.create_promo(
        code=request.code,
        discount=request.discount,
        expiry=request.expiry,
        assigned_users=request.assigned_users
    )
