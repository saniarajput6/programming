# PERSONAL EXPENSE TRACKER

expenses = []


# Display the main menu
def display_menu():
    print("\n================================")
    print("       PERSONAL EXPENSE TRACKER")
    print("================================")
    print("1. Add New Expense")
    print("2. View All Expenses")
    print("3. View Total Spending")
    print("4. Search Expenses by Category")
    print("5. Delete an Expense")
    print("6. Exit")
    print("================================")


# Add a new expense
def add_expense():
    print("\n--- ADD NEW EXPENSE ---")

    name = input("Enter expense name: ").strip()
    category = input("Enter expense category: ").strip()

    if name == "" or category == "":
        print("Name and category cannot be empty.")
        return

    try:
        amount = float(input("Enter amount spent (KSh): "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        expense = {
            "name": name,
            "category": category,
            "amount": amount
        }

        expenses.append(expense)

        print("\nExpense successfully recorded!")

    except ValueError:
        print("Invalid amount. Please enter a number.")


# View all recorded expenses
def view_expenses():
    print("\n--- ALL RECORDED EXPENSES ---")

    if len(expenses) == 0:
        print("No expenses have been recorded.")
        return

    for index, expense in enumerate(expenses, start=1):
        print("\nExpense Number:", index)
        print("Name:", expense["name"])
        print("Category:", expense["category"])
        print("Amount: KSh", expense["amount"])

    print("\nTotal number of expenses:", len(expenses))


# Calculate total spending
def calculate_total():
    print("\n--- TOTAL SPENDING ---")

    total = 0

    for expense in expenses:
        total = total + expense["amount"]

    print("Total Spending: KSh", round(total, 2))


# Search expenses by category
def search_category():
    print("\n--- SEARCH EXPENSES ---")

    category = input("Enter category to search: ").strip()

    found = False

    for expense in expenses:

        if expense["category"].lower() == category.lower():

            print("\nExpense:", expense["name"])
            print("Category:", expense["category"])
            print("Amount: KSh", expense["amount"])

            found = True

    if found == False:
        print("No expenses found in this category.")


# Delete an expense
def delete_expense():
    print("\n--- DELETE EXPENSE ---")

    if len(expenses) == 0:
        print("There are no expenses to delete.")
        return

    view_expenses()

    try:
        number = int(input("\nEnter expense number to delete: "))

        if number >= 1 and number <= len(expenses):

            removed = expenses.pop(number - 1)

            print(removed["name"], "has been successfully deleted.")

        else:
            print("Invalid expense number.")

    except ValueError:
        print("Please enter a valid number.")


# Main program
def main():

    while True:

        display_menu()

        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            calculate_total()

        elif choice == "4":
            search_category()

        elif choice == "5":
            delete_expense()

        elif choice == "6":
            print("\nThank you for using Personal Expense Tracker!")
            print("Goodbye!")
            break

        else:
            print("\nInvalid choice. Please select between 1 and 6.")


# Start the program
main()