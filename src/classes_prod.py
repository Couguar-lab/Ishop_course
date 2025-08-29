from abc import ABC, abstractmethod
from typing import List


class BaseProduct(ABC):

    @abstractmethod
    def __str__(self) -> str:
        pass


class MixinInfo:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        repr(self)

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        args = ", ".join(repr(arg) for arg in self._get_init_args())
        kwargs = ", ".join(f"{k}={repr(v)}" for k, v in self._get_init_kwargs().items())
        params = ", ".join(filter(None, [args, kwargs]))
        return f"{class_name}({params})"

    def _get_init_args(self):
        """Вспомогательный метод для получения аргументов __init__."""
        return []

    def _get_init_kwargs(self):
        """Вспомогательный метод для получения именованных аргументов __init__."""
        return {}


class Product(MixinInfo, BaseProduct):
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

    def _get_init_args(self):
        return [self.name, self.description, self.__price, self.quantity]

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

    def __str__(self) -> str:
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other) -> float:
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product")
        if type(self) != type(other):
            raise TypeError(f"Можно складывать только объекты одного класса. {type(self)} != {type(other)}")
        return (self.price * self.quantity) + (other.price * other.quantity)


class Smartphone(Product):
    efficiency: float
    model: str
    memory: int
    color: str

    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = float(efficiency)
        self.model = str(model)
        self.memory = int(memory)
        self.color = str(color)

    def _get_init_args(self):
        return super()._get_init_args()

    def _get_init_kwargs(self):
        return {"efficiency": self.efficiency, "model": self.model, "memory": self.memory, "color": self.color}

    def __str__(self) -> str:
        base_str = super().__str__()
        return f"{base_str} (Модель: {self.model}, Память: {self.memory}GB, Цвет: {self.color}, Производительность: {self.efficiency})"


class LawnGrass(Product):
    country: str
    germination_period: str
    color: str

    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = str(country)
        self.germination_period = str(germination_period)
        self.color = str(color)

    def _get_init_args(self):
        return super()._get_init_args()

    def _get_init_kwargs(self):
        return {"country": self.country, "germination_period": self.germination_period, "color": self.color}

    def __str__(self) -> str:
        base_str = super().__str__()
        return f"{base_str} (Страна: {self.country}, Прорастание: {self.germination_period}, Цвет: {self.color})"


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

    def add_product(self, product) -> None:
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product или его наследников")
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

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self):
        """Возвращает итератор по продуктам категории."""
        return CategoryIterator(self.__products)  # Передаем список напрямую


class CategoryIterator:
    def __init__(self, products):
        self._products = products  # Принимаем список продуктов
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self._products):
            raise StopIteration
        product = self._products[self.index]
        self.index += 1
        return product


class Order:
    def __init__(self, product: BaseProduct, quantity: int):
        if not isinstance(product, BaseProduct):
            raise TypeError("Продукт должен наследовать BaseProduct")
        if quantity <= 0 or quantity > product.quantity:
            raise ValueError("Недопустимое количество")
        self.product = product
        self.quantity = int(quantity)
        self._total_cost = product.price * quantity

    def get_name(self) -> str:
        return self.product.name

    def get_total_quantity(self) -> int:
        return self.quantity

    @property
    def total_cost(self) -> float:
        return self._total_cost

    def __str__(self) -> str:
        return f"Заказ: {self.product.name}, Кол-во: {self.quantity}, Итог: {self.total_cost} руб."

    def __repr__(self):
        return f"Order('{self.product.name}', '{self.product.description}', {self.product.price}, {self.quantity})"
