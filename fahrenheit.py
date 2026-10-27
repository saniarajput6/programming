fehrenheit = float (input("enter temperature in fehrenheit"))

def fehrenheit_to_celcius(fehrenheit):
    return (fehrenheit - 32) * 5 / 9

celcius = fehrenheit_to_celcius(fehrenheit)
print (f" {fehrenheit} fehrenheit equal to {celcius:.2f} celcius.")
