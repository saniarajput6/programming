from random import randint
min_str = input("min: ")
max_str = input("max: ")
minimum = int(min_str)
maximum = int(max_str)
random1 = randint(minimum, maximum)
random2 = randint(minimum, maximum)
usernumber = input("what is your lucky number?: ")
lucky_number = int(usernumber)
if lucky_number == random1 or lucky_number == random2:
    print("Today is your lucky day! :")
else:
    print("better luck next time! :")