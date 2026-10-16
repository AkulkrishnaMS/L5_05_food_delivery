"""Manage orders for a simple food-delivery system."""
import json
import pickle
from datetime import datetime

# Global state
orders = {}

menu = {}
VALID_STATUSES = ["placed", "cooking", "out_for_delivery", "delivered"]

def create_order(customer, items, order_history=None):
    """Create an order and return its ID."""
    if order_history is None:
        order_history = []

    order_id = max(orders, default=0) + 1
    total = 0

    for i in items:
        total += menu.get(i, 99)

    orders[order_id] = {
        "customer": customer,
        "items": items,
        "total": total,
        "status": "placed",
    }

    order_history.append(order_id)
    return order_history[-1]


def update_order_status(order_id, status):
    if order_id in orders:
        orders[order_id]["status"] = status


def read_menu_config(file="menu.json"):
    global menu
    try:
        f = open(file)
        menu = json.load(f)
    except Exception:
        menu = {"pizza": 250, "burger": 150, "fries": 90, "coke": 40}

def daily_revenue():
    revenue = 0
    for o in orders:
        if orders[o]["status"] == "delivered":
            revenue = revenue + orders[o]["total"]
    return revenue

def backup_orders(file="orders.pkl"):
    f = open(file, "wb")
    pickle.dump(orders, f)
    f.close()

def restore_orders(file="orders.pkl"):
    global orders
    orders = pickle.load(open(file, "rb"))

def printQueue():
    print("Order queue at %s" % datetime.now())
    for o in orders:
        print(o, orders[o]["customer"], orders[o]["status"], orders[o]["total"])

def main():
    read_menu_config()
    a = create_order("Asha", ["pizza", "coke"])
    b = create_order("Ravi", ["burger", "sushi"])
    c = create_order("", [])
    update_order_status(a, "delivered")
    update_order_status(b, "teleported")
    update_order_status(42, "delivered")
    update_order_status(c, "delivered")
    print("Revenue today:", daily_revenue())
    backup_orders()
    restore_orders()
    printQueue()

main()
