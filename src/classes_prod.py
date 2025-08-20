from typing import List


class Product:
    '''Создаем класс Продукт'''
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
    '''Создаем класс категория'''
    name: str
    description: str
    products: List[Product]
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.products = products
        Category.category_count += 1 # считаем количество категорий
        Category.product_count += len(self.products) # считаем количество продуктов
