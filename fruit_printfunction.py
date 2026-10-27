def print_list(items, header=None) :
    if header != None :
        print(header)

    for item in items :
        print(f"{item}")
    print()

names = ["Sania", "Arwa", "Baljot", "Sahil", "Joseph", "Abdirahman", "Abdirahim", "Shivam", "Hussein", "Divit"]

names.append("Toothless")
names.append("Hiccup")
names.append("Astrid")

print_list(names)
print_list(names, "NAMES")
names.sort()
print_list(names, "NAMES sorted")
names.reverse()
print_list(names, "NAMES reversed")


names.insert(0, "Toothless")
print(f"{names.count('Toothless')} Toothless")

while "Toothless" in names :
    names.remove("Toothless")

print_list(names, "NAMES after removing Toothless")

    
