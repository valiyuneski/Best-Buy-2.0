class Product:
    """Represents a product with a name, price, and quantity.
    Attributes:
        name (str): The name of the product.
        price (float): The price of the product.
        quantity (int): The available quantity of the product.
        active (bool): Indicates whether the product is active."""

    def __init__(self, name: str, price: float, quantity: int):
        if not name.strip():
            raise ValueError("Product name cannot be empty.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True if quantity > 0 else False

    def get_quantity(self) -> int:
        """Returns the product's quantity."""
        return self.quantity

    def set_quantity(self, quantity):
        """Sets the product's quantity. Quantity cannot be negative."""
        if quantity >= 0:
            self.quantity = quantity
        else:
            raise ValueError("Quantity cannot be negative")

    def is_active(self) -> bool:
        """Returns True if the product is active, False otherwise."""
        return self.active

    def set_active(self, active: bool):
        """Sets the product's active status."""
        self.active = active

    def activate(self):
        """Activates the product."""
        self.set_active(True)

    def deactivate(self):
        """Deactivates the product."""
        self.set_active(False)

    def show(self):
        """Returns a string representing the product."""
        return f"{self.name}, Price: ${self.price:.2f}, Quantity: {self.quantity}, Active: {'Yes' if self.active else 'No'}"

    def purchase(self, amount: int):
        if not self.active:
            raise ValueError("Cannot purchase inactive product.")
        if amount <= 0:
            raise ValueError("Purchase amount must be positive.")
        if amount > self.quantity:
            raise ValueError("Not enough quantity available.")

        self.quantity -= amount
        if self.quantity == 0:
            self.active = False
        return self.price * amount