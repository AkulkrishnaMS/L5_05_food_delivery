
"""Manage orders for a simple food-delivery system."""

import json
from datetime import datetime

DEFAULT_MENU = {
    "pizza": 250,
    "burger": 150,
    "fries": 90,
    "coke": 40,
}

VALID_STATUSES = {
    "placed",
    "cooking",
    "out_for_delivery",
    "delivered",
}

orders = {}
menu = DEFAULT_MENU.copy()


def create_order(customer, items, order_history=None):
    """Create an order and return its ID."""
    if order_history is None:
        order_history = []

    if not isinstance(customer, str) or not customer.strip():
        raise ValueError("Customer name cannot be empty.")

    if not isinstance(items, list) or not items:
        raise ValueError("An order must contain at least one item.")

    unknown_items = [
        item for item in items
        if not isinstance(item, str) or item not in menu
    ]
    if unknown_items:
        names = ", ".join(str(item) for item in unknown_items)
        raise ValueError(f"Unknown menu items: {names}")

    order_id = max(orders, default=0) + 1
    total = sum(menu[item] for item in items)

    orders[order_id] = {
        "customer": customer,
        "items": items.copy(),
        "total": total,
        "status": "placed",
    }

    order_history.append(order_id)
    return order_id


def update_order_status(order_id, status):
    """Update the status of an existing order."""
    if order_id not in orders or status not in VALID_STATUSES:
        return False

    orders[order_id]["status"] = status
    return True


def read_menu_config(file="menu.json"):
    """Load the menu from JSON or use the built-in menu as a fallback."""
    try:
        with open(file, "r", encoding="utf-8") as menu_file:
            loaded_menu = json.load(menu_file)

        if not isinstance(loaded_menu, dict) or not loaded_menu:
            raise ValueError("Menu must be a non-empty JSON object.")

        valid_menu = all(
            isinstance(name, str)
            and isinstance(price, (int, float))
            and not isinstance(price, bool)
            and price >= 0
            for name, price in loaded_menu.items()
        )
        if not valid_menu:
            raise ValueError("Menu prices must be non-negative numbers.")

    except (OSError, ValueError):
        loaded_menu = DEFAULT_MENU.copy()

    menu.clear()
    menu.update(loaded_menu)


def daily_revenue():
    """Calculate revenue from orders marked as delivered."""
    return sum(
        order["total"]
        for order in orders.values()
        if order["status"] == "delivered"
    )


def backup_orders(file="orders.json"):
    """Save the current orders to a JSON backup."""
    with open(file, "w", encoding="utf-8") as backup_file:
        json.dump(orders, backup_file, indent=2)


def restore_orders(file="orders.json"):
    """Restore orders from a JSON backup."""
    with open(file, "r", encoding="utf-8") as backup_file:
        loaded_orders = json.load(backup_file)

    if not isinstance(loaded_orders, dict):
        raise ValueError("Backup must contain a JSON object.")

    try:
        restored_orders = {
            int(order_id): order
            for order_id, order in loaded_orders.items()
        }
    except (TypeError, ValueError) as error:
        raise ValueError("Backup contains invalid order IDs.") from error

    if any(
        not isinstance(order, dict)
        for order in restored_orders.values()
    ):
        raise ValueError("Backup contains invalid order records.")

    orders.clear()
    orders.update(restored_orders)


def print_queue():
    """Print all current orders."""
    print(f"Order queue at {datetime.now()}")
    for order_id, order in orders.items():
        print(
            order_id,
            order["customer"],
            order["status"],
            order["total"],
        )


def main():
    """Run a demonstration of the food-delivery system."""
    read_menu_config()

    first_order = create_order("Asha", ["pizza", "coke"])
    second_order = create_order("Ravi", ["burger", "fries"])

    update_order_status(first_order, "delivered")
    update_order_status(second_order, "out_for_delivery")

    print("Revenue today:", daily_revenue())
    backup_orders()
    restore_orders()
    print_queue()


if __name__ == "__main__":
    main()
