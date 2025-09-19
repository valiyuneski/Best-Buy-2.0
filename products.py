# ------------------ PRODUCT TYPES ------------------
class Product:
    def __init__(self, name, price, quantity, promotion=None):
        if not name:
            raise ValueError("Product name cannot be empty!")
        if price < 0:
            raise ValueError("Product price cannot be negative!")

        self.name = name
        self._price = price
        self.quantity = quantity  # None for unlimited
        self._promotion = promotion

    # price property
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Product price cannot be negative!")
        self._price = value

    # promotion property
    @property
    def promotion(self):
        return self._promotion

    @promotion.setter
    def promotion(self, promo):
        self._promotion = promo

    def __str__(self):
        q_str = "Unlimited" if self.quantity is None else str(self.quantity)
        promo_str = f" Promotion: {self.promotion}" if self.promotion else " Promotion: None"
        return f"{self.name}, Price: ${self.price} Quantity:{q_str}{promo_str}"

    def calculate_price(self, amount):
        if self.promotion:
            return self.promotion.apply_promotion(self, amount)
        return amount * self.price

    def reduce_stock(self, amount):
        if self.quantity is not None:
            if amount > self.quantity:
                raise ValueError("Not enough stock!")
            self.quantity -= amount

    def is_active(self):
        if self.quantity is None:
            return True
        return self.quantity > 0

    # compare by price
    def __lt__(self, other):
        return self.price < other.price

    def __gt__(self, other):
        return self.price > other.price


class NonStockedProduct(Product):
    def __init__(self, name, price, promotion=None):
        super().__init__(name, price, quantity=0, promotion=promotion)

    def reduce_stock(self, amount):
        return

    def is_active(self):
        return True

    def __str__(self):
        return super().__str__() + " (Non-Stocked Product)"


class LimitedProduct(Product):
    def __init__(self, name, price, quantity, maximum, promotion=None):
        super().__init__(name, price, quantity, promotion)
        self.maximum = maximum

    def reduce_stock(self, amount):
        if amount > self.maximum:
            raise ValueError(f"This product is limited to {self.maximum} per order!")
        super().reduce_stock(amount)

    def __str__(self):
        return super().__str__() + f" (Limited to {self.maximum} per order)"
