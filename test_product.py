import pytest
from products import Product


def test_product_initialization():
    """Testing that a new product is initialized correctly """
    product = Product("new item", 999, quantity = 3)

    assert product.name == "new item"
    assert product.price == 999
    assert product.quantity == 3

def test_product_invalid_name():
    """ Testing if ValueError is raised when name is empty """
    with pytest.raises(ValueError):
        Product("", 50, quantity = 3)

def test_product_invalid_price():
    """ Testing if ValueError is raised when price is negative """
    with pytest.raises(ValueError):
        Product("item", -50, quantity = 3)

def test_product_quantity():
    """ Testing that product becomes inactive when quantity reaches zero"""
    product = Product("item", 999, quantity = 10)

    product.set_quantity(10)
    assert product.quantity == 0
    assert product.active is False

def test_quantity_modified_after_purchase():
    """ Testing that the quantity is modified (reduced) after an order """
    product = Product("item", 999, quantity=1000)

    product.buy(999)
    assert product.quantity == 1
    with pytest.raises(ValueError):
        Product("item", -50, quantity = 3)

def test_error_raised_after_too_large_purchase():
    """ Testing that the quantity is not modified when ordered
    more than there is on stock --> raise ValueError"""
    product = Product("item", 999, quantity=1000)

    with pytest.raises(ValueError):
        product.buy(1001)
