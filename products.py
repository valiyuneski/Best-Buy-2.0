class Product:
    """ Represents a product with a name, price, and quantity.
    The product becomes inactive when its quantity reaches zero. """

    def __init__(self, name, price, quantity):
        """Initialize a product with name, price, quantity."""
        if not isinstance(name, str) or not name:
            raise ValueError("Product name must be a non-empty string.")

        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a positive number.")

        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity must be a non-negative integer.")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = quantity > 0
        self.promotion = None


    def set_promotion(self, promotion):
        """ Sets a promotion for a certain product. """

        self.promotion = promotion


    def get_price(self, quantity) -> float:
        """ Returns the price after applying the promotion. """

        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        return self.price * quantity


    def get_quantity(self) -> int:
        """Returns the current quantity of the product. """

        return self.quantity


    def set_quantity(self, quantity):
        """Reduces the product's quantity and deactivates it
        if it reaches zero. """

        self.quantity -= quantity
        if self.quantity <= 0:
            self.deactivate()


    def is_active(self) -> bool:
        """Returns whether the product is active
        (available for purchase or not)."""

        return self.active

    def activate(self):
        """ Activates the product. """

        self.active = True


    def deactivate(self):
        """ Deactivates the product. """

        self.active = False


    def show(self) -> str:
        """ Returns a string including information about the
        available product, it's price and promo(if there is one) """

        promo_info = f" {self.promotion.name}" if self.promotion else ""
        return (f"{self.name}, Price: {self.price} €, "
                f"Quantity: {self.quantity} pcs{promo_info}")


    def buy(self, quantity) -> float:
        """ Processes the purchase of a product of the passed quantity. """
        if quantity > self.quantity:
            raise ValueError("Not enough stock available.")
        total_price = quantity * self.price
        self.set_quantity(quantity)
        return total_price


class LimitedProduct(Product):
    """ Sub-class inheriting (from class Product) modified to handle
    products with a maximum order volume such as a shipping fee"""

    def __init__(self, name, price, quantity, maximum = 1):
        super().__init__(name, price, quantity)
        self.maximum = maximum

    def show(self):
        return super().show() + f" (maximum: {self.maximum})"

    def buy(self, quantity) -> float:
        if quantity > self.maximum:
            raise ValueError(f"You can only buy up to {self.maximum} of"
                             f" '{self.name}' per order.")

        return super().buy(quantity)


class NonStockedProduct(Product):
    """ Class inheriting (from class Product) modified to handle
    products without the need of stock such as a Windows license
    or e-books etc... """

    def __init__(self, name, price):
        super().__init__(name, price, quantity=0)

    def is_active(self) -> bool:
        """Returns that NonStockProducts are always active."""

        return True

    def show(self):
        """Displays that there is no quantity available,
        but that it's unlimited."""

        return f"{self.name}, Price: {self.price} €, (unlimited quantity)"


    def set_quantity(self, quantity):
        """ NonStockProducts quantity can not be set because
        it's 0 all the time."""

        raise NotImplementedError("NonStockProduct has unlimited stock and "
                                  "quantity cannot be set.")

    def get_quantity(self) -> int:
        """ Returns 0 because it's an unlimited product. """

        return 0

    def buy(self, quantity) -> float:
        """ Processes a purchase of an unlimited quantity product.
        (no stock to reduce) """

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero for "
                             "non-stock products.")

        total_price = quantity * self.price
        return total_price
