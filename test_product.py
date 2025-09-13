# pytest -v

import pytest
from products import Product
from promotions import Promotion, PercentDiscount, SecondHalfPrice, ThirdOneFree

def test_create_normal_product():
    """Test creating a normal product."""
    p = Product("Laptop", price=1200, quantity=10)
    assert p.name == "Laptop"
    assert p.price == 1200
    assert p.quantity == 10
    assert p.active is True

def test_create_product_invalid_name():
    """Test creating a product with an invalid (empty) name."""
    with pytest.raises(ValueError, match="Product name cannot be empty."):
        Product("", price=1450, quantity=100)

def test_create_product_negative_price():
    """Test creating a product with a negative price."""
    with pytest.raises(ValueError, match="Price cannot be negative."):
        Product("MacBook Air M2", price=-10, quantity=100)

def test_product_becomes_inactive_at_zero_quantity():
    """Test that a product becomes inactive when its quantity reaches zero."""
    p = Product("Phone", price=800, quantity=1)
    p.purchase(1)
    assert p.quantity == 0
    assert p.active is False

def test_product_purchase_updates_quantity_and_returns_total():
    """Test purchasing a product updates quantity and returns total cost."""
    p = Product("Tablet", price=500, quantity=5)
    total = p.purchase(2)
    assert total == 1000
    assert p.quantity == 3
    assert p.active is True

def test_buy_more_than_available_raises_exception():
    """Test that buying more than available quantity raises an exception."""
    p = Product("Headphones", price=100, quantity=2)
    with pytest.raises(ValueError, match="Not enough quantity available."):
        p.purchase(3)

def test_purchase_from_inactive_product_raises_exception():
    """Test that purchasing from an inactive product raises an exception."""
    p = Product("Old Model", price=300, quantity=0)
    assert p.active is False
    with pytest.raises(ValueError, match="Cannot purchase inactive product."):
        p.purchase(1)


########
# setup initial stock of inventory
# product_list = [
#     Product("MacBook Air M2", price=1450, quantity=100),
#     Product("Bose QuietComfort Earbuds", price=250, quantity=500),
#     Product("Google Pixel 7", price=500, quantity=250),
#     Product("Windows License", price=125),  # NonStockedProduct could extend Product
#     Product("Shipping", price=10, quantity=250),  # LimitedProduct could extend Product
# ]

# # Create promotion catalog
# second_half_price = SecondHalfPrice("Second Half price!")
# third_one_free = ThirdOneFree("Third One Free!")
# thirty_percent = PercentDiscount("30% off!", percent=30)

# # Add promotions to products
# product_list[0].set_promotion(second_half_price)
# product_list[1].set_promotion(third_one_free)
# product_list[3].set_promotion(thirty_percent)

# # Example usage
# print(product_list[0].show())  # MacBook Air with Second Half price promotion
# print(product_list[1].show())  # Bose Earbuds with Third One Free promotion
# print(product_list[3].show())  # Windows License with 30% off

# # Simulate buying
# print("Buying 2 MacBooks:", product_list[0].buy(2))  # one full, one half
# print("Buying 3 Bose:", product_list[1].buy(3))      # pay only for 2
# print("Buying 1 Windows License:", product_list[3].buy(1))  # 30% discount
########

def test_percent_discount():
    product = Product("Windows License", price=100, quantity=10)
    promo = PercentDiscount("30% off!", percent=30)
    product.set_promotion(promo)

    total = product.buy(2)  # 2 * 100 * 0.7 = 140
    assert total == pytest.approx(140.0)
    assert product.quantity == 8


def test_second_half_price():
    product = Product("MacBook Air M2", price=1000, quantity=10)
    promo = SecondHalfPrice("Second Half price!")
    product.set_promotion(promo)

    total = product.buy(2)  # 1 * 1000 + 1 * 500 = 1500
    assert total == pytest.approx(1500.0)
    assert product.quantity == 8

    total = product.buy(3)  # 2 items → 1500, +1 item full price → 2500
    assert total == pytest.approx(2500.0)
    assert product.quantity == 5


def test_third_one_free():
    product = Product("Bose Earbuds", price=200, quantity=9)
    promo = ThirdOneFree("Third One Free!")
    product.set_promotion(promo)

    total = product.buy(3)  # pay for 2 → 400
    assert total == pytest.approx(400.0)
    assert product.quantity == 6

    total = product.buy(5)  # 3 items → pay for 2 (400), +2 items (400) = 800
    assert total == pytest.approx(800.0)
    assert product.quantity == 1


def test_no_promotion():
    product = Product("Google Pixel 7", price=500, quantity=5)
    total = product.buy(2)  # no promo → 2 * 500 = 1000
    assert total == pytest.approx(1000.0)
    assert product.quantity == 3


def test_not_enough_stock():
    product = Product("Shipping", price=10, quantity=1)
    with pytest.raises(ValueError):
        product.buy(2)

pytest.main()