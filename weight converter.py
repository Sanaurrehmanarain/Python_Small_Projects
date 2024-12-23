# Python weight converter

weight = float(input("Enter your weight: "))
unit = input("Kilograms or pounds? (K or L): ")

if unit == "K":
    weight = weight * 2.205
    unit = "Lbs."
    print("Your weight is: " , (round(weight, 1)), unit)

    # you can use f string also to print the same statement
    #print(f"Your weight is: {round(weight, 1)} {unit}")

elif unit == "L":
    weight = weight / 2.205
    unit = "kgs."
    print("Your weight is: " , (round(weight, 1)), unit)

else:
    print(f"{unit} was not valid")


