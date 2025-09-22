from products import NonStockedProduct
from products import LimitedProduct


class Store:
    """ Manages the products of the store and their quantity
    and handles ordering. """

    def __init__(self, products=None):
        """ Initializes the store with a list of products. """

        self.products = products if products is not None else []

    def add_product(self, product):
        """ Adds a product to the store. """

        self.products.append(product)


    def remove_product(self, product):
        """ Removes a product from the store. """

        if product in self.products:
            self.products.remove(product)


    def get_total_quantity(self) -> int:
        """ Returns the total quantity of all products in the store. """

        return sum(product.get_quantity() for product in self.products)


    def get_all_products(self):
        """Returns a list of all active products in the store."""
        return [product for product in self.products if product.is_active()]

    def process_order(self):
        """ Handles the complete order process, including user input,
        validation, and purchase. """

        shopping_list = []
        available_products = self.get_all_products()
        temporary_stock = {product: product.get_quantity() for product
                           in available_products}

        print("\nAvailable Products:")
        for index, product in enumerate(available_products):
            print(f"{index + 1}: {product.show()}")

        while True:


            print("\nPress enter to quit order process ...\n")
            product_number = input("Which product # do you want?: ").strip()

            if not product_number:
                break

            try:
                product_number = int(product_number)

                if product_number <= 0 or product_number > len(available_products):
                    print("\nInvalid product number!\n")
                    continue

                order_quantity = int(input("\nWhat amount do you want?: ").strip())

                if order_quantity <= 0:
                    print("\nQuantity must be positive!\n")
                    continue

                selected_product = available_products[product_number - 1]

                if isinstance(selected_product, LimitedProduct):
                    if order_quantity > selected_product.maximum:
                        print(f"\nYou can only order up to "
                              f"{selected_product.maximum} of "
                              f"{selected_product.name}.")
                        continue

                if isinstance(selected_product, NonStockedProduct):
                    temporary_stock[selected_product] = float('inf')
                    print(f"\n{selected_product.name} has unlimited stock! "
                          f"You can buy as many as you like.")

                if order_quantity > temporary_stock[selected_product]:
                    print(f"\nNot enough items in stock - only "
                          f"{temporary_stock[selected_product]} left!\n")
                    continue

                temporary_stock[selected_product] -= order_quantity
                shopping_list.append((selected_product, order_quantity))
                print(f"\n{selected_product.name} (qty: {order_quantity}) "
                      f"added to your basket!\n")

            except ValueError:
                print("\nYou must enter valid numbers!\n")

        if shopping_list:
            total_price = self.order(shopping_list)
            print(f"\nOrder complete! Total price: {total_price} €\n")
        else:
            print("Your shopping basket is empty. Shopping process stopped.")

    def order(self, shopping_list) -> float:
        """ Processes an order and returns the total price, applying promotions. """

        total_price = 0
        for product, quantity in shopping_list:
            if not product.is_active():
                print(f"Warning: {product.name} is inactive and cannot be ordered.")
                continue

            # Calculate the total price considering the promotion
            total_price_for_product = product.get_price(quantity)

            # After calculating the price, now reduce the quantity of the product
            product.buy(quantity)

            # Add the price to the total
            total_price += total_price_for_product

        return total_price

