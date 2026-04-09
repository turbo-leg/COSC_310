# pylint: disable=too-many-locals, too-many-branches, too-many-nested-blocks, consider-using-enumerate
"""
Handles logic for admin statistics.
"""

from typing import Optional
from datetime import datetime
from app import database

class AdminService:
    """
    Handles logic for generating admin statistics.
    """

    def get_stats(
        self, start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        status: Optional[str] = None
    ):
        """
        Calculates and returns platform statistics.
        """
        users = database.get_all_users(skip=0, limit=1000000)
        total_users = len(users)

        orders = database.get_all_orders()

        filtered_orders_list = []

        for order in orders:
            keep_order = True

            if status is not None:
                if order.get("status") != status:
                    keep_order = False
            if start_date is not None or end_date is not None:
                if order.get("createdAt") is None:
                    keep_order = False
                else:
                    try:
                        created_str = order.get("createdAt")
                        if created_str is not None:
                            order_date = datetime.fromisoformat(str(created_str))

                            if start_date is not None:
                                start_date_obj = datetime.fromisoformat(str(start_date))
                                if order_date < start_date_obj:
                                    keep_order = False

                            if end_date is not None:
                                end_date_obj = datetime.fromisoformat(str(end_date))
                                if order_date > end_date_obj:
                                    keep_order = False
                    except ValueError:
                        pass

            if keep_order is True:
                filtered_orders_list.append(order)

        total_orders_count = 0
        for _ in filtered_orders_list:
            total_orders_count = total_orders_count + 1

        menu_items = database.get_all_menu_items()

        total_menu_items_count = len(menu_items)

        calculated_revenue = 0.0

        for order in filtered_orders_list:
            items_list = order.get("items", [])
            for i in range(len(items_list)):
                current_item_id = items_list[i]

                db_menu_item = database.get_menu_item_by_id(current_item_id)

                if db_menu_item is not None:
                    item_price = db_menu_item.get("price", 0.0)
                    calculated_revenue = calculated_revenue + item_price

        return {
            "total_users": total_users,
            "total_orders": total_orders_count,
            "total_revenue": round(calculated_revenue, 2),
            "total_menu_items": total_menu_items_count
        }

    def create_promo(self, code: str, discount: float, expiry: str, assigned_users):
        """
        Handles logic for creating promo codes
        """
        existing = database.get_promo_code(code)
        if existing:
            raise ValueError("Promo code already exists")
        return database.create_promo_code(code, discount, expiry, assigned_users)

admin_service = AdminService()
