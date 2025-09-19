from products import Product, NonStockedProduct, LimitedProduct
from promotions import SecondHalfPrice, ThirdOneFree, ThirdOneFree, PercentDiscount
from store import Store
import pytest

# ------------------ TESTS ------------------

def test_create_normal_product():
    """Test creating a normal product."""
    product = Product("MacBook Air M2", price=1450, quantity=100)
    assert product.name == "MacBook Air M2"
    assert product.price == 1450
    assert product.quantity == 100


def test_create_product_invalid_empty_name():
    """Test creating a product with an empty name raises ValueError."""
    with pytest.raises(ValueError):
        Product("", price=1450, quantity=100)


def test_create_product_invalid_negative_price():
    """Test creating a product with a negative price raises ValueError."""
    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=-10, quantity=100)


def test_product_becomes_inactive_at_zero():
    """Test that a product becomes inactive when quantity reaches zero."""
    product = Product("Google Pixel 7", price=500, quantity=1)
    product.reduce_stock(1)
    assert product.is_active() is False


def test_product_purchase_modifies_quantity_and_price():
    """Test that purchasing a product modifies its quantity and calculates price correctly."""
    product = Product("Bose QuietComfort Earbuds", price=250, quantity=10)
    product.reduce_stock(2)
    assert product.quantity == 8
    assert product.calculate_price(2) == 500


def test_buying_more_than_stock_raises():
    """Test that trying to buy more than available stock raises ValueError."""
    product = Product("MacBook Air M2", price=1450, quantity=5)
    with pytest.raises(ValueError):
        product.reduce_stock(10)


# ------------------ PROMOTION TESTS ------------------

def test_second_half_price_promotion():
    """Test the Second Half Price promotion."""
    promo = SecondHalfPrice("Second Half price!")
    product = Product("MacBook Air M2", price=100, quantity=10, promotion=promo)
    assert product.calculate_price(1) == 100
    assert product.calculate_price(2) == 150
    assert product.calculate_price(3) == 250


def test_third_one_free_promotion():
    """Test the Third One Free promotion."""
    promo = ThirdOneFree("Third One Free!")
    product = Product("Bose Earbuds", price=50, quantity=10, promotion=promo)
    assert product.calculate_price(1) == 50
    assert product.calculate_price(2) == 100
    assert product.calculate_price(3) == 100
    assert product.calculate_price(6) == 200


def test_percent_discount_promotion():
    """Test the Percent Discount promotion."""
    promo = PercentDiscount("30% off!", percent=30)
    product = Product("Windows License", price=100, quantity=None, promotion=promo)
    assert product.calculate_price(1) == 70
    assert product.calculate_price(3) == 210


# ------------------ NEW PRODUCT TYPES TESTS ------------------

def test_non_stocked_product_always_active():
    """Test that a non-stocked product is always active and quantity remains zero."""
    product = NonStockedProduct("Windows License", price=125)
    assert product.quantity == 0
    assert product.is_active() is True
    product.reduce_stock(10)
    assert product.quantity == 0


def test_limited_product_rejects_exceeding_order():
    """Test that a limited product rejects orders exceeding the maximum limit."""
    product = LimitedProduct("Shipping", price=10, quantity=10, maximum=1)
    with pytest.raises(ValueError):
        product.reduce_stock(2)


def test_limited_product_allows_valid_order():
    """Test that a limited product allows orders within the maximum limit."""
    product = LimitedProduct("Shipping", price=10, quantity=10, maximum=1)
    product.reduce_stock(1)
    assert product.quantity == 9


# ------------------ MAGIC METHODS TESTS ------------------

def test_price_setter_rejects_negative():
    """Test that setting a negative price raises ValueError."""
    product = Product("MacBook Air M2", price=1450, quantity=100)
    with pytest.raises(ValueError):
        product.price = -100


def test_str_magic_method():
    """Test the string representation of a product."""
    product = Product("MacBook Air M2", price=1450, quantity=100)
    result = str(product)
    assert "MacBook Air M2" in result
    assert "$1450" in result


def test_comparison_magic_methods():
    """Test the comparison magic methods based on price."""
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    assert mac > bose
    assert not (bose > mac)


def test_in_operator_and_add_operator():
    """Test the 'in' operator for Store and the '+' operator to combine stores."""
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    pixel = Product("Google Pixel 7", price=500, quantity=250)
    best_buy = Store([mac, bose])
    assert mac in best_buy
    assert pixel not in best_buy

    other_store = Store([pixel])
    combined = best_buy + other_store
    assert len(combined.products) == 3