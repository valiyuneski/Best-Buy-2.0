from products import Product

# ------------------ STORE ------------------
class Store:
    """A store containing multiple products."""
    def __init__(self, products=None):
        """Initialize the store with a list of products."""
        if products is None:
            self.products = [
                Product("MacBook Air M2", 1450, 100, "Second Half price!"),
                Product("Bose QuietComfort Earbuds", 250, 500, "Third One Free!"),
                Product("Google Pixel 7", 500, 250),
                Product("Windows License", 125, None, "30% off!"),
                Product("Shipping", 10, 1, None),
            ]
        else:
            self.products = products

    def __contains__(self, product):
        """Check if a product is in the store."""
        return product in self.products

    def __add__(self, other):
        """Combine two stores into one."""
        return Store(self.products + other.products)

    def __str__(self):
        """String representation of the store."""
        return f"Store with {len(self.products)} products"

    def list_products(self):
        """List all products in the store."""
        for i, p in enumerate(self.products, start=1):
            print(f"{i}. {p}")

    def total_items(self):
        """Calculate total number of items in stock (excluding non-stocked)."""
        total = 0
        for p in self.products:
            if p.quantity is not None:
                total += p.quantity
        return total

    def make_order(self):
        """Interactively make an order from the store."""
        order = []
        while True:
            self.list_products()
            choice = input("Which product # do you want? (empty to finish) ").strip()
            if choice == "":
                break

            try:
                idx = int(choice) - 1
                product = self.products[idx]
            except (ValueError, IndexError):
                print("Invalid product number!")
                continue

            try:
                amount = int(input("What amount do you want? "))
            except ValueError:
                print("Invalid amount!")
                continue

            try:
                product.reduce_stock(amount)
                order.append((product, amount))
                print("Product added to list!")
            except ValueError as e:
                print(e)

        total_payment = sum(p.calculate_price(a) for p, a in order)
        print("********")
        print(f"Order made! Total payment: ${total_payment:.0f}")