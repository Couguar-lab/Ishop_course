from typing import List


class Product:
    """Создаем класс Продукт"""

    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
        self.name = str(name)
        self.description = str(description)
        self.__price = float(price)
        self.quantity = int(quantity)

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float, confirm: bool = None) -> None:
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        elif value < self.__price:
            if confirm is not None:  # Для тестов
                print(f"Цена понижается с {self.__price} до {value}. Подтверждение: {confirm}")
                if confirm:
                    self.__price = value
                else:
                    print("Понижение цены отменено")
            else:  # Для реального использования
                confirmation = input(f"Цена понижается с {self.__price} до {value}. Подтвердить (y/n)? ").lower()
                if confirmation == "y":
                    self.__price = value
                else:
                    print("Понижение цены отменено")
        else:
            self.__price = value

    @classmethod
    def new_product(cls, product_data: dict, existing_products: List["Product"] = None) -> "Product":
        name = str(product_data.get("name", ""))
        description = str(product_data.get("description", ""))
        price = float(product_data.get("price", 0.0))
        quantity = int(product_data.get("quantity", 0))

        if existing_products:
            for product in existing_products:
                if product.name == name:
                    product.quantity += quantity
                    product.price = max(product.price, price)
                    return product

        return cls(name, description, price, quantity)


class Category:
    """Создаем класс Категория"""

    name: str
    description: str
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.__products = []
        Category.category_count += 1  # считаем количество категорий

    def add_product(self, product: Product) -> None:
        if isinstance(product, Product):
            self.__products.append(product)
            Category.product_count += 1  # увеличиваем количество категорий на 1

    @property
    def products_list(self) -> str:
        if not self.__products:
            return "Нет товаров в категории."
        return "\n".join(f"{p.name}, {p.price} руб. Остаток: {p.quantity} шт." for p in self.__products)

    @property
    def products(self) -> List[Product]:
        return self.__products.copy()
