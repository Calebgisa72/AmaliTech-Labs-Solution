from .services.customer_service import CustomerService
from .services.product_service import ProductService
from .services.order_service import OrderService
from .analytics.reports import AnalyticsReports
from .utils.common import setup_logger

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


def add_item_to_cart():
    try:
        cid = input("Enter customer ID (Session ID): ")
        pid = int(input("Enter product ID: "))
        qty = int(input("Enter quantity: "))

        prod = product_service.get_product(pid)
        if prod:
            price = prod["price"]
            item = {
                "product_id": pid,
                "quantity": qty,
                "price": price,
                "name": prod["name"],
            }
            order_service.add_to_cart(cid, item)
            print(f"Added {prod['name']} (x{qty}) to cart.")
        else:
            print("Product not found.")
    except ValueError as ve:
        print(f"Input Error: {ve}")
    except Exception as e:
        print(f"Error adding to cart: {e}")
        logger.error(f"Error adding to cart: {e}")


def view_cart():
    try:
        cid = input("Enter customer ID (Session ID): ")
        cart_items = order_service.get_cart(cid)
        if not cart_items:
            print("Cart is empty.")
            return

        print(f"\n--- Cart for Customer {cid} ---")
        for i, item in enumerate(cart_items, 1):
            name = item.get("name", f"Product {item['product_id']}")
            print(
                f"{i}. {name} (ID: {item['product_id']}) - Qty: {item['quantity']} - ${item['price']:.2f}"
            )
        print("-------------------------------")
    except Exception as e:
        print(f"Error viewing cart: {e}")
        logger.error(f"Error viewing cart: {e}")


def remove_item_from_cart():
    try:
        cid = input("Enter customer ID (Session ID): ")
        pid = int(input("Enter product ID to remove: "))
        order_service.remove_from_cart(cid, pid)
        print(f"Removed product {pid} from cart.")
    except ValueError as ve:
        print(f"Input Error: {ve}")
    except Exception as e:
        print(f"Error removing item: {e}")
        logger.error(f"Error removing item: {e}")


def checkout():
    try:
        cid = int(input("Enter customer ID to checkout: "))
        # Assuming customer ID matches the session ID used for cart
        session_id = str(cid)

        cart_items = order_service.get_cart(session_id)
        if not cart_items:
            print("Cart is empty. Nothing to checkout.")
            return

        # Validate stock before proceeding (optional but good practice)
        # The create_order method already checks stock, so we rely on that.

        oid = order_service.create_order(cid, cart_items)
        print(f"Order placed successfully! Order ID: {oid}")

        # Clear cart after successful order
        order_service.clear_cart(session_id)

    except ValueError as ve:
        print(f"Input Error: {ve}")
    except Exception as e:
        print(f"Checkout Error: {e}")
        logger.error(f"Checkout Error: {e}")


def get_top_selling_products():
    try:
        limit = input("Enter limit (default 10): ")
        limit = int(limit) if limit else 10
        results = analytics_service.get_top_selling_products(limit)
        print(f"\nTop {limit} Selling Products:")
        for item in results:
            print(f"{item['product']}: {item['total_sold']} sold")
    except Exception as e:
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
