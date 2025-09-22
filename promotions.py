from abc import ABC, abstractmethod

class Promotions(ABC):
    """ Abstract parent class for general promotions to apply"""

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity) -> float:
        pass

class PercentageDiscount(Promotions):
    """ Sub-class handling promotions in terms of
    adding a %- discount to a product price """

    def __init__(self, name, discount_percent):
        super().__init__(name)
        self.discount_percent = discount_percent

    def apply_promotion(self, product, quantity) -> float:
        discount = product.price * (self.discount_percent / 100)
        return (product.price - discount) * quantity

class SecondItemHalfPrice(Promotions):
    """ Sub-class handling promotions in terms of
    reducing the product price of every second product """

    def __init__(self, name):
        super().__init__(name)

    def apply_promotion(self, product, quantity) -> float:
        full_price_items_count = (quantity // 2) + (quantity % 2)
        half_price_items_count = (quantity // 2)

        discounted_price = ((full_price_items_count * product.price) +
                            (half_price_items_count * (product.price * 0.5)))

        return discounted_price


class Buy1Get1Free(Promotions):
    """ Sub-class handling promotions in terms of
    not to apply the product price to every second product """

    def __init__(self, name):
        super().__init__(name)

    def apply_promotion(self, product, quantity) -> float:
        payable_quantity = (quantity // 2) + (quantity % 2)
        return payable_quantity * product.price