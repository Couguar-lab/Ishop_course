import pytest

from src.classes_prod import Category, Product


@pytest.fixture
def product():
    return Product(
        name="Samsung Galaxy S23 Ultra", description="256GB, Серый цвет, 200MP камера", price=10000.0, quantity=5
    )


@pytest.fixture
def category(product):
    return Category(
        name="Смартфоны",
        description="Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        products=[product],
    )
