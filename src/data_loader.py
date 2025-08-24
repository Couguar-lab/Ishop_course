import json
from pathlib import Path
from typing import List

from src.classes_prod import Category, Product


def load_data_from_json(file_path: str = "data/products.json", raise_exceptions: bool = True) -> List[Category]:
    """Функция загрузки данных из json-файла"""
    file_path = Path(__file__).parent.parent / file_path
    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        if raise_exceptions:
            raise
        return []
    except json.JSONDecodeError:
        if raise_exceptions:
            raise
        return []

    categories = []
    for category_data in data:
        category = Category(name=category_data["name"], description=category_data["description"])
        for product_data in category_data.get("products", []):
            product = Product.new_product(product_data, category.products)
            category.add_product(product)
        categories.append(category)

    return categories
