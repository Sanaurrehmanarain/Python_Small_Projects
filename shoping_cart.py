# Shopping cart program

foods = []
prices = []
total = 0

while True:
    food = input("Enter a food to buy (q to quit): ")
    if food.lower() == "q":    # if the user input capital Q, this function set it to the lower q.
        break
    else:
        price = float(input(f"Enter the price of a {food}: $"))
        foods.append(food)          # append food to the foods list
        prices.append(price)        # append price to the prices list

print("----- YOUR CART -----")

for food in foods:
    print(food)

for price in prices:
    total += price

print(f"Your total is: ${total}")