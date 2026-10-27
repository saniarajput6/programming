size = int(input("what size square? "))
for row in range(size):
    output = ""
    for column in range(size):
        output += "*"
    print(output)

print()
input("press return to continue ...")