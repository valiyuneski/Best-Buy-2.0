# ------------------ PRODUCT TYPES ------------------
class Product:
    """A product available in the store."""
    def __init__(self, name, price, quantity, promotion=None):
        """Initialize a product with name, price, quantity, and optional promotion."""
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
        """Get or set the price of the product."""
        return self._price

    @price.setter
    def price(self, value):
        """Set a new price for the product."""
        if value < 0:
            raise ValueError("Product price cannot be negative!")
        self._price = value

    # promotion property
    @property
    def promotion(self):
        """Get or set the promotion for the product."""
        return self._promotion

    @promotion.setter
    def promotion(self, promo):
        """Set a new promotion for the product."""
        self._promotion = promo

    def __str__(self):
        """String representation of the product."""
        q_str = "Unlimited" if self.quantity is None else str(self.quantity)
        promo_str = f" Promotion: {self.promotion}" if self.promotion else " Promotion: None"
        return f"{self.name}, Price: ${self.price} Quantity:{q_str}{promo_str}"

    def calculate_price(self, amount):
        """Calculate total price for given amount, applying promotion if any."""
        if self.promotion:
            return self.promotion.apply_promotion(self, amount)
        return amount * self.price

    def reduce_stock(self, amount):
        """Reduce stock by amount, if applicable."""
        if self.quantity is not None:
            if amount > self.quantity:
                raise ValueError("Not enough stock!")
            self.quantity -= amount

    def is_active(self):
        """A product is active if it has stock or is non-stocked."""
        if self.quantity is None:
            return True
        return self.quantity > 0

    def __lt__(self, other):
        """Less than comparison based on price."""
        return self.price < other.price

    def __gt__(self, other):
        """Greater than comparison based on price."""
        return self.price > other.price


class NonStockedProduct(Product):
    """A product that is always in stock (e.g., digital goods)."""
    def __init__(self, name, price, promotion=None):
        """Non-stocked products have unlimited quantity."""
        super().__init__(name, price, quantity=0, promotion=promotion)

    def reduce_stock(self, amount):
        """Non-stocked products do not reduce stock."""
        return

    def is_active(self):
        """Non-stocked products are always active."""
        return True

    def __str__(self):
        """String representation indicating non-stocked status."""
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
