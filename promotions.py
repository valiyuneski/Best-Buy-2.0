from abc import ABC, abstractmethod
# ------------------ PROMOTIONS ------------------
class Promotion(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity):
        pass

    def __str__(self):
        return self.name


class PercentDiscount(Promotion):
    def __init__(self, name, percent):
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product, quantity):
        return product.price * quantity * (1 - self.percent / 100)


class SecondHalfPrice(Promotion):
    def apply_promotion(self, product, quantity):
        full_price = (quantity // 2 + quantity % 2) * product.price
        half_price = (quantity // 2) * (product.price / 2)
        return full_price + half_price


class ThirdOneFree(Promotion):
    def apply_promotion(self, product, quantity):
        paid_items = quantity - (quantity // 3)
        return paid_items * product.price
