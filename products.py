class Product:
    def __init__(self, name, price, quantity, promotion=None):
        if not name:
            raise ValueError("Product name cannot be empty!")
        if price < 0:
            raise ValueError("Product price cannot be negative!")

        self.name = name
        self.price = price
        self.quantity = quantity  # None for unlimited
        self.promotion = promotion

    def __str__(self):
        q_str = "Unlimited" if self.quantity is None else str(self.quantity)
        promo_str = f" Promotion: {self.promotion}" if self.promotion else " Promotion: None"
        return f"{self.name}, Price: ${self.price}, Quantity: {q_str},{promo_str}"

    def calculate_price(self, amount):
        if self.promotion == "Second Half price!":
            full_price = (amount // 2 + amount % 2) * self.price
            half_price = (amount // 2) * (self.price / 2)
            return full_price + half_price

        elif self.promotion == "Third One Free!":
            paid_items = amount - (amount // 3)
            return paid_items * self.price

        elif self.promotion == "30% off!":
            return amount * self.price * 0.7

        else:
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


class NonStockedProduct(Product):
    def __init__(self, name, price, promotion=None):
        super().__init__(name, price, quantity=0, promotion=promotion)

    def reduce_stock(self, amount):
        # Stock does not change
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
