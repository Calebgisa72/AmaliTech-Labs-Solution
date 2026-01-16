from src.utils.setup_db import init_db
import random
from faker import Faker
from src.services.customer_service import CustomerService
from src.services.product_service import ProductService
from src.services.order_service import OrderService
from src.utils.common import setup_logger
import src.controllers as ctrl

logger = setup_logger(__name__)


def seed_data():
    fake = Faker()
    customer_service = CustomerService()
    product_service = ProductService()
    order_service = OrderService()

    logger.info("Checking if seeding is required...")
    products = product_service.get_all_products()
    if products:
        logger.info("Data already exists. Skipping seeding.")
        return

    logger.info("Seeding data...")

    # Seed Products
    categories = ["Electronics", "Clothing", "Home", "Books", "Sports"]
    products = []
    for _ in range(20):
        name = f"Product {fake.random_company_product().capitalize()} {fake.word().capitalize()}"
        category = random.choice(categories)
        price = float(fake.random_int(min=10, max=500))
        stock = random.randint(10, 100)
        metadata = {"description": fake.sentence(), "brand": fake.company()}

        try:
            pid = product_service.add_product(name, category, price, stock, metadata)
            products.append({"id": pid, "price": price})
        except Exception as e:
            logger.error(f"Failed to seed product: {e}")

    logger.info(f"Seeded {len(products)} products.")

    # Seed Customers
    customers = []
    for _ in range(10):
        name = fake.name()
        email = fake.unique.email()
        try:
            cid = customer_service.create_customer(name, email)
            customers.append(cid)
        except Exception as e:
            logger.error(f"Failed to seed customer: {e}")

    logger.info(f"Seeded {len(customers)} customers.")

    # Seed Orders
    if products and customers:
        for _ in range(15):
            customer_id = random.choice(customers)
            # Create a random cart
            cart_items = []
            num_items = random.randint(1, 5)
            selected_products = random.sample(products, num_items)

            for prod in selected_products:
                qty = random.randint(1, 3)
                cart_items.append(
                    {"product_id": prod["id"], "quantity": qty, "price": prod["price"]}
                )

            try:
                order_service.create_order(customer_id, cart_items)
            except Exception as e:
                logger.error(f"Failed to seed order: {e}")

        logger.info("Seeded orders.")

    logger.info("Seeding complete.")


def print_menu():
    print("\n--- E-Commerce Analytics Data Pipeline ---")
    print("1. Add Customer")
    print("2. Add Product")
    print("3. Add Item to Cart")
    print("4. View Cart")
    print("5. Remove Item from Cart")
    print("6. Checkout (Place Order)")
    print("7. View Top Selling Products")
    print("8. View Products Ranked by Category")
    print("9. View Customer LTV (Total Revenue)")
    print("10. Exit")
    print("------------------------------------------")


def interactive_menu():
    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            ctrl.add_customer()
        elif choice == "2":
            ctrl.add_product()
        elif choice == "3":
            ctrl.add_item_to_cart()
        elif choice == "4":
            ctrl.view_cart()
        elif choice == "5":
            ctrl.remove_item_from_cart()
        elif choice == "6":
            ctrl.checkout()
        elif choice == "7":
            ctrl.get_top_selling_products()
        elif choice == "8":
            ctrl.get_products_ranked_by_category()
        elif choice == "9":
            ctrl.get_customer_ltv()
        elif choice == "10":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    try:
        # Initialize Database
        init_db()

        # Seed Data
        seed_data()

        # Start Menu
        interactive_menu()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        logger.error(f"Application crash: {e}")
        print("Application crashed. Check logs for details.")


if __name__ == "__main__":
    main()
