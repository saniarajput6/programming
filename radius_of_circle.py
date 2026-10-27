def circle_area(radius):
    return 3.14159 * radius * radius

print(circle_area(5))
print(circle_area(10))
print(circle_area(15))

radius = float(input("enter the radius of the circle: "))
area = circle_area(radius)
print(f"the area of the circle with radius {radius} is: {area}")
    
