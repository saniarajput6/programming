print("WELCOME TO SIMPLE ATM")

balance = 5000

print("1. Check Balance")
print("2. Withdraw Money")

choice = input("Choose an option: ")

if choice == "1":
    print("Your balance is:", balance)

elif choice == "2":
    amount = float(input("Enter withdrawal amount: "))

    if amount <= balance and amount > 0:
        balance = balance - amount
        print("Withdrawal successful!")
        print("Remaining balance:", balance)

    else:
        print("Insufficient balance or invalid amount.")

else:
    print("Invalid option.")