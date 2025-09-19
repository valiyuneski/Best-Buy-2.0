from store import Store


def main():
    """Main function to run the store CLI."""
    store = Store()

    while True:
        print("\n   Store Menu")
        print("   ----------")
        print("1. List all products in store")
        print("2. Show total amount in store")
        print("3. Make an order")
        print("4. Quit")
        choice = input("Please choose a number: ").strip()

        if choice == "1":
            store.list_products()
        elif choice == "2":
            print(f"Total of {store.total_items()} items in store")
        elif choice == "3":
            store.make_order()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()