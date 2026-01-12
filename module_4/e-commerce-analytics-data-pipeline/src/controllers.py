from src.services.customer_service import CustomerService
from src.services.product_service import ProductService
from src.services.order_service import OrderService
from src.analytics.reports import AnalyticsReports
from src.utils.common import setup_logger

logger = setup_logger(__name__)

customer_service = CustomerService()
product_service = ProductService()
order_service = OrderService()
analytics_service = AnalyticsReports()


def add_customer():
    try:
        name = input("Enter customer name: ")
        email = input("Enter customer email: ")
        cid = customer_service.create_customer(name, email)
        print(f"Customer created successfully with ID: {cid}")
    except Exception as e:
        print(f"Error adding customer: {e}")
        logger.error(f"Error adding customer: {e}")


def add_product():
    try:
        name = input("Enter product name: ")
        category = input("Enter category: ")
        price = float(input("Enter price: "))
        stock = int(input("Enter stock quantity: "))
        desc = input("Enter description (optional): ")
        metadata = {"description": desc} if desc else {}
        pid = product_service.add_product(name, category, price, stock, metadata)
        print(f"Product created successfully with ID: {pid}")
    except ValueError as ve:
        print(f"Input Error: {ve}")
    except Exception as e:
        print(f"Error adding product: {e}")
        logger.error(f"Error adding product: {e}")


def place_order():
    try:
        cid = int(input("Enter customer ID: "))
        cart_items = []
        while True:
            pid = int(input("Enter product ID to buy (or 0 to finish): "))
            if pid == 0:
                break
            qty = int(input("Enter quantity: "))

            prod = product_service.get_product(pid)
            if prod:
                price = prod["price"]
                cart_items.append({"product_id": pid, "quantity": qty, "price": price})
                print(f"Added {prod['name']} to cart.")
            else:
                print("Product not found.")

        if cart_items:
            oid = order_service.create_order(cid, cart_items)
            print(f"Order placed successfully! Order ID: {oid}")
        else:
            print("No items in order.")
    except ValueError as ve:
        print(f"Input Error: {ve}")
    except Exception as e:
        print(f"Error placing order: {e}")
        logger.error(f"Error placing order: {e}")


def get_top_selling_products():
    try:
        limit = input("Enter limit (default 10): ")
        limit = int(limit) if limit else 10
        results = analytics_service.get_top_selling_products(limit)
        print(f"\nTop {limit} Selling Products:")
        for item in results:
            print(f"{item['product']}: {item['total_sold']} sold")
    except Exception as e:
        print(f"Error fetching top selling products: {e}")
        logger.error(f"Error fetching top selling products: {e}")


def get_products_ranked_by_category():
    try:
        results = analytics_service.get_products_ranked_by_category()
        print("\nProducts Ranked by Category:")
        current_cat = None
        for item in results:
            if item["category"] != current_cat:
                current_cat = item["category"]
                print(f"\n--- {current_cat} ---")
            print(f"Rank {item['rank']}: {item['product']} (Sold: {item['sold']})")
    except Exception as e:
        print(f"Error fetching ranked products: {e}")
        logger.error(f"Error fetching ranked products: {e}")


def get_customer_ltv():
    try:
        results = analytics_service.get_customer_total_revenue()
        print("\nCustomer Lifetime Value:")
        for item in results:
            print(f"{item['customer']}: ${item['total_revenue']:.2f}")
    except Exception as e:
        print(f"Error fetching customer LTV: {e}")
        logger.error(f"Error fetching customer LTV: {e}")
