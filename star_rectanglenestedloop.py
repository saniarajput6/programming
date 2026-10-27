rows = int(input("how many rows? "))
cols = int(input("how many columns? "))
for row in range(rows):
    output = ""
    for col in range(cols):
        output += "*"
    print(output)

print()
input("press return to continue ...")