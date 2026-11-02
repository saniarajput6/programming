print("STUDENT GRADE CALCULATOR")
print("------------------------")

name = input("Enter student name: ")

maths = float(input("Enter Maths marks: "))
english = float(input("Enter English marks: "))
ict = float(input("Enter ICT marks: "))

# Calculate the average
total = maths + english + ict
average = total / 3

# Determine the grade
if average >= 70:
    grade = "A"
elif average >= 60:
    grade = "B"
elif average >= 50:
    grade = "C"
elif average >= 40:
    grade = "D"
else:
    grade = "F"

print("\n----- STUDENT RESULTS -----")
print("Student Name:", name)
print("Total Marks:", total)
print("Average Marks:", round(average, 2))
print("Grade:", grade)

if average >= 40:
    print("Result: PASS")
else:
    print("Result: FAIL")

print("---------------------------")
print("Thank you for using the calculator!")