from src.classes_prod import Category, Product


def test_product_initialization(product):
    assert product.name == "Samsung Galaxy S23 Ultra"
    assert product.description == "256GB, Серый цвет, 200MP камера"
    assert product.price == 10000.0
    assert product.quantity == 5


def test_category_initialization(category, product):
    assert category.name == "Смартфоны"
    assert (
        category.description
        == "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни"
    )
    assert category.products == [product]
    assert len(category.products) == 1


def test_category_count():
    Category.category_count = 0
    category1 = Category("Smartphone", "Xiaomi", [])
    category2 = Category("Laptop", "Asus", [])
    assert Category.category_count == 2


def test_product_count(product):
    Category.product_count = 0
    products = [product, Product("Xiaomi", "Smartphone", 10000.0, 5)]
    category = Category("Smartwatch", "Gadgets", products)
    assert Category.product_count == 2
