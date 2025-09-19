from products import Product

# ------------------ STORE ------------------
class Store:
    def __init__(self, products=None):
        self.products = products or []

    def __contains__(self, product):
        return product in self.products

    def __add__(self, other):
        return Store(self.products + other.products)

    def __str__(self):
        return f"Store with {len(self.products)} products"

    def list_products(self):
        if not self.products:
            print("No products in store.")
            return
        for idx, product in enumerate(self.products, start=1):
            status = "Active" if product.is_active() else "Inactive"
            print(f"{idx}. {product} - Status: {status}")

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