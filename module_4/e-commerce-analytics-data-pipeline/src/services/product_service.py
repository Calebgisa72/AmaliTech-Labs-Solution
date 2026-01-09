from src.database.postgres import PostgresDB


class ProductService:
    def add_product(
        self, name: str, category: str, price: float, stock: int, metadata: dict
    ):
        # TODO: Insert product into Postgres
        pass

    def get_product(self, product_id: int):
        # TODO: Get product details
        pass

    def update_stock(self, product_id: int, quantity: int):
        # TODO: Update stock level
        pass
