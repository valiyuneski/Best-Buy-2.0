from products import Product
import pytest
# ------------------ TESTS ------------------

def test_create_normal_product():
    product = Product("MacBook Air M2", price=1450, quantity=100)
    assert product.name == "MacBook Air M2"
    assert product.price == 1450
    assert product.quantity == 100


def test_create_product_invalid_empty_name():
    with pytest.raises(ValueError):
        Product("", price=1450, quantity=100)


def test_create_product_invalid_negative_price():
    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=-10, quantity=100)


def test_product_becomes_inactive_at_zero():
    product = Product("Google Pixel 7", price=500, quantity=1)
    product.reduce_stock(1)
    assert product.is_active() is False


def test_product_purchase_modifies_quantity_and_price():
    product = Product("Bose QuietComfort Earbuds", price=250, quantity=10)
    product.reduce_stock(2)
    assert product.quantity == 8
    assert product.calculate_price(2) == 500


def test_buying_more_than_stock_raises():
    product = Product("MacBook Air M2", price=1450, quantity=5)
    with pytest.raises(ValueError):
        product.reduce_stock(10)


# ------------------ PROMOTION TESTS ------------------

def test_second_half_price_promotion():
    product = Product("MacBook Air M2", price=100, quantity=10, promotion="Second Half price!")
    assert product.calculate_price(1) == 100  # single item full price
    assert product.calculate_price(2) == 150  # second item half price
    assert product.calculate_price(3) == 250


def test_third_one_free_promotion():
    product = Product("Bose Earbuds", price=50, quantity=10, promotion="Third One Free!")
    assert product.calculate_price(1) == 50
    assert product.calculate_price(2) == 100
    assert product.calculate_price(3) == 100  # third is free
    assert product.calculate_price(6) == 200  # 2 free items


def test_thirty_percent_off_promotion():
    product = Product("Windows License", price=100, quantity=None, promotion="30% off!")
    assert product.calculate_price(1) == 70
    assert product.calculate_price(3) == 210