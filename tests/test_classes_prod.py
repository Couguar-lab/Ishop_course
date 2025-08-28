import pytest

from src.classes_prod import Category, LawnGrass, Product, Smartphone


def test_product_initialization(product):
    assert product.name == "Samsung Galaxy S23 Ultra"
    assert product.description == "256GB, Серый цвет, 200MP камера"
    assert product.price == 10000.0
    assert product.quantity == 5


def test_category_initialization(category, product):
    assert category.name == "Смартфоны"
    assert (
        category.description
        == """Смартфоны, 
        как средство не только коммуникации, но и получения дополнительных функций для удобства жизни"""
    )
    category.add_product(product)
    assert category.products_list == "Samsung Galaxy S23 Ultra, 10000.0 руб. Остаток: 5 шт."


def test_category_count():
    Category.category_count = 0
    category1 = Category("Smartphone", "Xiaomi")
    category2 = Category("Laptop", "Asus")
    assert Category.category_count == 2


def test_product_count(product):
    Category.product_count = 0
    category = Category("Electronics", "Gadgets")
    category.add_product(product)
    category.add_product(Product("Phone", "Smartphone", 500.0, 5))
    assert Category.product_count == 2


def test_private_products_access():
    category = Category("Test", "Test Category")
    with pytest.raises(AttributeError):
        category.__products  # Проверка приватности
    product = Product("Test Product", "Test", 100.0, 5)
    category.add_product(product)
    assert "Test Product" in category.products_list  # Доступ через геттер


def test_add_product():
    Category.product_count = 0
    category = Category("Test", "Test Category")
    product = Product("Test Product", "Test", 100.0, 5)
    category.add_product(product)
    assert category.products_list == "Test Product, 100.0 руб. Остаток: 5 шт."
    assert Category.product_count == 1


def test_new_product():
    product_data = {"name": "New Product", "description": "New Description", "price": 200.0, "quantity": 3}
    product = Product.new_product(product_data)
    assert product.name == "New Product"
    assert product.description == "New Description"
    assert product.price == 200.0
    assert product.quantity == 3


def test_new_product_with_duplicates():
    category = Category("Test", "Test Category")
    product1_data = {"name": "Duplicate", "description": "First", "price": 100.0, "quantity": 5}
    product2_data = {"name": "Duplicate", "description": "Second", "price": 150.0, "quantity": 3}
    product1 = Product.new_product(product1_data)
    category.add_product(product1)
    product2 = Product.new_product(product2_data, category.products)
    assert product2.quantity == 8  # 5 + 3
    assert product2.price == 150.0  # Максимальная цена
    assert category.products_list == "Duplicate, 150.0 руб. Остаток: 8 шт."


def test_price_setter_positive():
    product = Product("Test", "Test", 100.0, 5)
    product.price = 150.0
    assert product.price == 150.0


def test_price_setter_negative_or_zero(capsys):
    product = Product("Test", "Test", 100.0, 5)
    product.price = 0
    assert product.price == 100.0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out


def test_price_setter_decrease_reject(monkeypatch, capsys):
    product = Product("Test", "Test", 100.0, 5)
    monkeypatch.setattr("builtins.input", lambda *args: "n")
    product.price = 80.0
    assert product.price == 100.0
    captured = capsys.readouterr()
    assert "Понижение цены отменено" in captured.out


def test_product_str():
    product = Product("Laptop", "High-end laptop", 999.99, 10)
    assert str(product) == "Laptop, 999.99 руб. Остаток: 10 шт."


def test_category_str():
    category = Category("Electronics", "Gadgets")
    product1 = Product("Laptop", "High-end", 1000.0, 5)
    product2 = Product("Phone", "Smartphone", 500.0, 3)
    category.add_product(product1)
    category.add_product(product2)
    assert str(category) == "Electronics, количество продуктов: 8 шт."


def test_product_add():
    product1 = Product("Laptop", "High-end", 100.0, 10)
    product2 = Product("Phone", "Smartphone", 200.0, 2)
    result = product1 + product2
    assert result == (100.0 * 10) + (200.0 * 2)  # 1000 + 400 = 1400
    with pytest.raises(TypeError):
        product1 + "not a product"  # Проверка на неверный тип


def test_category_iterator():
    category = Category("Electronics", "Gadgets")
    product1 = Product("Laptop", "High-end", 1000.0, 5)
    product2 = Product("Phone", "Smartphone", 500.0, 3)
    category.add_product(product1)
    category.add_product(product2)
    products = [p for p in category]
    assert len(products) == 2
    assert products[0].name == "Laptop"
    assert products[1].name == "Phone"


def test_smartphone_init():
    phone = Smartphone("iPhone", "Smartphone", 999.99, 10, efficiency=5.0, model="X", memory=128, color="Silver")
    assert phone.name == "iPhone"
    assert phone.price == 999.99
    assert phone.quantity == 10
    assert phone.efficiency == 5.0
    assert phone.model == "X"
    assert phone.memory == 128
    assert phone.color == "Silver"
    assert (
        str(phone)
        == "iPhone, 999.99 руб. Остаток: 10 шт. (Модель: X, Память: 128GB, Цвет: Silver, Производительность: 5.0)"
    )


def test_lawn_grass_init():
    grass = LawnGrass("Green Lawn", "Grass", 19.99, 50, country="USA", germination_period="7 days", color="Green")
    assert grass.name == "Green Lawn"
    assert grass.price == 19.99
    assert grass.quantity == 50
    assert grass.country == "USA"
    assert grass.germination_period == "7 days"
    assert grass.color == "Green"
    assert str(grass) == "Green Lawn, 19.99 руб. Остаток: 50 шт. (Страна: USA, Прорастание: 7 days, Цвет: Green)"


def test_add_same_class():
    phone1 = Smartphone("iPhone", "Smartphone", 1000.0, 2, efficiency=5.0, model="X", memory=128, color="Silver")
    phone2 = Smartphone("iPhone", "Smartphone", 1000.0, 3, efficiency=5.0, model="X", memory=128, color="Silver")
    assert phone1 + phone2 == (1000.0 * 2) + (1000.0 * 3)  # 2000 + 3000 = 5000


def test_add_different_classes():
    phone = Smartphone("iPhone", "Smartphone", 1000.0, 2, efficiency=5.0, model="X", memory=128, color="Silver")
    grass = LawnGrass("Green Lawn", "Grass", 19.99, 50, country="USA", germination_period=7, color="Green")
    with pytest.raises(TypeError):
        phone + grass


def test_add_invalid_type():
    phone = Smartphone("iPhone", "Smartphone", 1000.0, 2, efficiency=5.0, model="X", memory=128, color="Silver")
    with pytest.raises(TypeError):
        phone + "not a product"


def test_add_product_restriction():
    category = Category("Electronics", "Gadgets")
    phone = Smartphone("iPhone", "Smartphone", 1000.0, 2, efficiency=5.0, model="X", memory=128, color="Silver")
    category.add_product(phone)
    assert "iPhone" in category.products_list
    with pytest.raises(TypeError):
        category.add_product("not a product")
