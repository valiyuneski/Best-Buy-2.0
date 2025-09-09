import pytest
from products import Product

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

pytest.main()