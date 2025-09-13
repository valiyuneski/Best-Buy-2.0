from abc import ABC, abstractmethod

class Promotion(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity: int) -> float:
        """Apply the promotion to the given product and quantity.
        Returns the discounted total price."""
        pass

    def __str__(self):
        return self.name


class PercentDiscount(Promotion):
    def __init__(self, name: str, percent: float):
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product, quantity: int) -> float:
        discount_multiplier = (100 - self.percent) / 100
        return product.price * quantity * discount_multiplier


class SecondHalfPrice(Promotion):
    def __init__(self, name: str):
        super().__init__(name)

    def apply_promotion(self, product, quantity: int) -> float:
        # For every 2 items, 1 is full price, 1 is half price
        pairs = quantity // 2
        remainder = quantity % 2
        total = (pairs * (product.price * 1.5)) + (remainder * product.price)
        return total


class ThirdOneFree(Promotion):
    def __init__(self, name: str):
        super().__init__(name)

    def apply_promotion(self, product, quantity: int) -> float:
        # For every 3 items, pay only for 2
        trios = quantity // 3
        remainder = quantity % 3
        total = (trios * 2 * product.price) + (remainder * product.price)
        return total


class PercentDiscount(Promotion):
    def __init__(self, name: str, percent: float):
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product, quantity: int) -> float:
        discount_multiplier = (100 - self.percent) / 100
        return product.price * quantity * discount_multiplier
