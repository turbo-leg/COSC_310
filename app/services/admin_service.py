"""
Handles logic for admin statistics.
"""

from app import database

class AdminService:
    """
    Handles logic for generating admin statistics.
    """

    def get_stats(self):
        """
        Calculates and returns platform statistics.
        """
        users = database.get_all_users(skip=0, limit=1000000)
        total_users = len(users)

        orders = database.get_all_orders()
        total_orders = len(orders)

        menu_items = database.get_all_menu_items()
        total_menu_items = len(menu_items)

        total_revenue = 0.0
        for order in orders:
            # Assuming order items is a list of item IDs or dicts
            items = order.get("items", [])
            for item_id in items:
                item = database.get_menu_item_by_id(item_id)
                if item:
                    total_revenue += item.get("price", 0.0)

        return {
            "total_users": total_users,
            "total_orders": total_orders,
            "total_revenue": round(total_revenue, 2),
            "total_menu_items": total_menu_items
        }
    
    def create_promo(self, code: str, discount: float, expiry: str, assigned_users):
        """
        Handles logic for creating promo codes
        """
        existing = database.get_promo_code(code)
        if existing:
            raise Exception("Promo code already exists")

        return database.create_promo_code(code, discount, expiry, assigned_users)

admin_service = AdminService()
