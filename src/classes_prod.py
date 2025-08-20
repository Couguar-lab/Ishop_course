class Product:
    name: str
    description: str
    price: float
    quantity: int
    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

class Category:
    name: str
    description: str
    products: list
    category_count: int
    product_count: int
    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.products = products
        self.category_count += 1
        self.product_count += 1
        # Category.category_count += 1
        # Category.product_count += 1