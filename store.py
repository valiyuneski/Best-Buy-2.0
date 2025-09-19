from products import Product

class Store:
    def __init__(self):
        self.products = [
            Product("MacBook Air M2", 1450, 100, "Second Half price!"),
            Product("Bose QuietComfort Earbuds", 250, 500, "Third One Free!"),
            Product("Google Pixel 7", 500, 250),
            Product("Windows License", 125, None, "30% off!"),
            Product("Shipping", 10, 1, None, limited_to=1),
        ]

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

            if product.limited_to and amount > product.limited_to:
                print(f"This product is limited to {product.limited_to} per order!")
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