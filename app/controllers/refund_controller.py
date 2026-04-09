"""
REST endpoints for the refund feature.
Users submit refund requests; admins view and resolve them.
"""
from typing import List

from fastapi import APIRouter
from app.schemas import RefundCreateRequest, RefundResponse, RefundUpdateRequest
from app.services.refund_service import request_refund, handle_refund
from app.services.refund_service import get_all_refunds
from app.services.refund_service import get_user_refunds
from app.auth_helpers import require_authenticated_user, require_admin

router = APIRouter(tags=["refunds"])


@router.post("/orders/{order_id}/refund", response_model=RefundResponse)
def create_refund_request(order_id: int, body: RefundCreateRequest):
    """
    Submits a refund request for a delivered and paid order.
    """
    require_authenticated_user(body.user_id)
    return request_refund(order_id, body.user_id, body.reason.value, body.description)


@router.get("/refunds", response_model=List[RefundResponse])
def list_refunds(user_id: int):
    """
    Returns all refund requests. Admin access only.
    """
    require_admin(user_id)
    return get_all_refunds()


@router.get("/refunds/user/{target_user_id}", response_model=List[RefundResponse])
def list_user_refunds(target_user_id: int):
    """
    Returns all refund requests submitted by the given user.
    """
    require_authenticated_user(target_user_id)
    return get_user_refunds(target_user_id)


@router.patch("/refunds/{refund_id}", response_model=RefundResponse)
def resolve_refund(refund_id: int, body: RefundUpdateRequest, user_id: int):
    """
    Approves or denies a refund request. Admin access only.
    """
    require_admin(user_id)
    return handle_refund(refund_id, body.status.value)
