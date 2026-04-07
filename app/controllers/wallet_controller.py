"""Endpoints for customer wallet operations."""

from fastapi import APIRouter, Depends
from app.auth import get_user
from app.schemas import WalletBalanceResponse, WalletTopUpRequest
from app.services.wallet_service import get_wallet_balance, top_up_wallet

router = APIRouter(prefix="/wallet", tags=["wallet"])


@router.get("/me", response_model=WalletBalanceResponse)
def read_wallet(user=Depends(get_user)):
    """Return the authenticated customer's wallet balance."""
    return get_wallet_balance(user)


@router.post("/top-up", response_model=WalletBalanceResponse)
def add_wallet_funds(request: WalletTopUpRequest, user=Depends(get_user)):
    """Top up the authenticated customer's wallet."""
    return top_up_wallet(user, request.amount)
