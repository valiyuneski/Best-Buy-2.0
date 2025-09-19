from abc import ABC, abstractmethod
# ------------------ PROMOTIONS ------------------
class Promotion(ABC):
    """Abstract base class for promotions."""
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity):
        """Apply the promotion to the product for the given quantity."""
        pass

    def __str__(self):
        """String representation of the promotion."""
        return self.name


class PercentDiscount(Promotion):
    """Percentage discount promotion."""
    def __init__(self, name, percent):
        """Initialize with name and discount percent."""
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product, quantity):
        """Apply percentage discount to the product price."""
        return product.price * quantity * (1 - self.percent / 100)


class SecondHalfPrice(Promotion):
    """Second item at half price promotion."""
    def apply_promotion(self, product, quantity):
        """Apply second half price promotion."""
        full_price = (quantity // 2 + quantity % 2) * product.price
        half_price = (quantity // 2) * (product.price / 2)
        return full_price + half_price


class ThirdOneFree(Promotion):
    """Third item free promotion."""
    def apply_promotion(self, product, quantity):
        """Apply third one free promotion."""
        paid_items = quantity - (quantity // 3)
        return paid_items * product.price
