def collatz(number):
    if number % 2 == 0:    # so we can know that we can evenly divide the number with 2
        result = number // 2
        print(result)
        return result
    else:
        result = 3 * number + 1
        print(result)
        return result

print("Enter number:")

try:
    number = int(input())
    while number != 1:
        number = collatz(number)

except ValueError:
    print("Invalid input. You must enter an integer.")