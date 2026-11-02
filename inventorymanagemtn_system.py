import json
import os

FILE_NAME = "inventory.json"

inventory = {}

def load_inventory():

    global inventory

    if os.path.exists(FILE_NAME):

        try:
            with open(FILE_NAME, "r") as file:
                inventory = json.load(file)

        except (json.JSONDecodeError, OSError):
            inventory = {}

    else:
        inventory = {}

def save_inventory():

    with open(FILE_NAME, "w") as file:
        json.dump(inventory, file, indent=4)

def display_menu():

    print("\n================================")
    print("       INVENTORY MANAGEMENT")
    print("================================")
    print("1. Add New Product")
    print("2. View All Products")
    print("3. Search for a Product")
    print("4. Update Product Quantity")
    print("5. Delete Product")
    print("6. View Low Stock Products")
    print("7. Exit")
    print("================================")

def add_product():

    print("\n--- ADD NEW PRODUCT ---")

    product_id = input("Enter product ID: ").strip()

    if product_id == "":
        print("Product ID cannot be empty.")
        return

    if product_id in inventory:
        print("A product with this ID already exists.")
        return

    name = input("Enter product name: ").strip()
    category = input("Enter product category: ").strip()

    if name == "" or category == "":
        print("Product name and category cannot be empty.")
        return

    try:
        price = float(input("Enter product price: KSh "))
        quantity = int(input("Enter product quantity: "))

        if price <= 0 or quantity < 0:
            print("Enter a valid price and quantity.")
            return

        inventory[product_id] = {
            "name": name,
            "category": category,
            "price": price,
            "quantity": quantity
        }

        save_inventory()

        print("Product successfully added!")

    except ValueError:
        print("Please enter valid numerical values.")

def view_products():

    print("\n--- PRODUCT INVENTORY ---")

    if not inventory:
        print("No products have been recorded.")
        return

    for product_id, product in inventory.items():

        print("\nProduct ID:", product_id)
        print("Name:", product["name"])
        print("Category:", product["category"])
        print("Price: KSh", product["price"])
        print("Quantity:", product["quantity"])
def search_product():

    print("\n--- SEARCH PRODUCT ---")

    search_id = input("Enter product ID: ").strip()

    if search_id in inventory:

        product = inventory[search_id]

        print("\nProduct Found!")
        print("Name:", product["name"])
        print("Category:", product["category"])
        print("Price: KSh", product["price"])
        print("Quantity:", product["quantity"])

    else:
        print("Product not found.")

def update_quantity():

    print("\n--- UPDATE PRODUCT QUANTITY ---")

    product_id = input("Enter product ID: ").strip()

    if product_id not in inventory:
        print("Product not found.")
        return

    print("Current quantity:", inventory[product_id]["quantity"])

    try:
        new_quantity = int(input("Enter new quantity: "))

        if new_quantity < 0:
            print("Quantity cannot be negative.")
            return

        inventory[product_id]["quantity"] = new_quantity

        save_inventory()

        print("Product quantity successfully updated.")

    except ValueError:
        print("Please enter a valid whole number.")


# Delete a product
def delete_product():

    print("\n--- DELETE PRODUCT ---")

    product_id = input("Enter product ID: ").strip()

    if product_id in inventory:

        confirmation = input(
            "Are you sure you want to delete this product? (yes/no): "
        ).lower().strip()

        if confirmation == "yes":

            del inventory[product_id]

            save_inventory()

            print("Product successfully deleted.")

        else:
            print("Deletion cancelled.")

    else:
        print("Product not found.")

def low_stock_products():

    print("\n--- LOW STOCK PRODUCTS ---")

    found = False

    for product_id, product in inventory.items():

        if product["quantity"] <= 5:

            print("\nProduct ID:", product_id)
            print("Name:", product["name"])
            print("Remaining quantity:", product["quantity"])

            found = True

    if not found:
        print("There are no products with low stock.")

def main():

    load_inventory()

    while True:

        display_menu()

        choice = input("Select an option (1-7): ").strip()

        if choice == "1":
            add_product()

        elif choice == "2":
            view_products()

        elif choice == "3":
            search_product()

        elif choice == "4":
            update_quantity()

        elif choice == "5":
            delete_product()

        elif choice == "6":
            low_stock_products()

        elif choice == "7":
            print("Thank you for using Inventory Management System!")
            break

        else:
            print("Invalid selection. Please choose between 1 and 7.")


main()