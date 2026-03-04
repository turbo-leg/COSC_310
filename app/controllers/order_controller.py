from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import OrderResponse
from app.services.order_service import get_orders_by_restaurant

router = APIRouter()

@router.get("/restaurants/{restaurant_id}/orders", response_model=List[OrderResponse])
def view_incoming_orders(restaurant_id: int, db: Session = Depends(get_db)):
    return get_orders_by_restaurant(db, restaurant_id)