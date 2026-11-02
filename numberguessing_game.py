# Number Guessing Game

def display_welcome():
    print("==============================")
    print("      NUMBER GUESSING GAME")
    print("==============================")
    print("Guess the secret number between 1 and 10.")
    print("You have 3 attempts to get it right!")
    print()


def play_game():
    secret_number = 7
    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:

        guess = int(input("Enter your guess: "))
        attempts += 1

        if guess == secret_number:
            print("\nCongratulations! You guessed correctly!")
            print("Number of attempts:", attempts)
            return

        elif guess < secret_number:
            print("Too low! Try a higher number.")

        else:
            print("Too high! Try a lower number.")

        remaining = max_attempts - attempts
        print("Attempts remaining:", remaining)
        print()

    print("\nGame over! You have run out of attempts.")
    print("Better luck next time!")


def main():
    display_welcome()

    play_again = "yes"

    while play_again.lower() == "yes":
        play_game()

        play_again = input("\nWould you like to play again? (yes/no): ")

    print("\nThank you for playing!")


main()