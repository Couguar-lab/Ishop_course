import pytest

from src.classes_prod import Category, Product
from src.data_loader import load_data_from_json


def test_load_data_from_json():
    # Сбрасываем счетчики перед тестом
    Category.category_count = 0
    Category.product_count = 0

    # Загружаем данные из JSON
    categories = load_data_from_json("data/products.json")

    # Проверяем, что список категорий содержит две категории
    assert len(categories) == 2
    category1, category2 = categories

    # Проверяем первую категорию "Смартфоны"
    assert category1.name == "Смартфоны"
    assert (
        category1.description
        == "Смартфоны, как средство не только коммуникации, но и получение дополнительных функций для удобства жизни"
    )
    assert len(category1.products) == 3

    # Проверяем продукты первой категории
    products1 = category1.products
    assert products1[0].name == "Samsung Galaxy C23 Ultra"
    assert products1[0].description == "256GB, Серый цвет, 200MP камера"
    assert products1[0].price == 180000.0
    assert products1[0].quantity == 5
    assert products1[1].name == "Iphone 15"
    assert products1[1].description == "512GB, Gray space"
    assert products1[1].price == 210000.0
    assert products1[1].quantity == 8
    assert products1[2].name == "Xiaomi Redmi Note 11"
    assert products1[2].description == "1024GB, Синий"
    assert products1[2].price == 31000.0
    assert products1[2].quantity == 14

    # Проверяем вторую категорию "Телевизоры"
    assert category2.name == "Телевизоры"
    assert (
        category2.description
        == "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником"
    )
    assert len(category2.products) == 1

    # Проверяем продукт второй категории
    products2 = category2.products
    assert products2[0].name == '55" QLED 4K'
    assert products2[0].description == "Фоновая подсветка"
    assert products2[0].price == 123000.0
    assert products2[0].quantity == 7

    # Проверяем подсчет категорий и продуктов
    assert Category.category_count == 2
    assert Category.product_count == 4  # 3 + 1 = 4 продукта
