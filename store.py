from products import Product

# ------------------ STORE ------------------
class Store:
    def __init__(self, products=None):
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
        return product in self.products

    def __add__(self, other):
        return Store(self.products + other.products)

    def __str__(self):
        return f"Store with {len(self.products)} products"

    def list_products(self):
        for i, p in enumerate(self.products, start=1):
            print(f"{i}. {p}")

    def total_items(self):
        total = 0
        for p in self.products:
            if p.quantity is not None:
                total += p.quantity
        return total

    def make_order(self):
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