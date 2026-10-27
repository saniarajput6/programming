n_lines = int(input("how many lines?"))
for counter in range(1, n_lines+1):
    if counter % 2 == 1:
        continue
    print(f"this is line{counter}")

print()
input("press return to continue ...")