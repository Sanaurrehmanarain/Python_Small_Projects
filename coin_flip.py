import random
numberOfstreaks = 0
containsStreak = False
coinFlip = []
streak = 0

for experimentNumber in range(10000):
    # code that creates a list of 100 'heads' or 'tails' values.
    for i in range(100):
        coinFlip.append(random.randint(0, 1))

    # code that checks if there is a streak of 6 heads or tails in a row.
    for i in range(len(coinFlip)):
        if i == 0:
            pass
        elif coinFlip[i] == coinFlip[i - 1]:
            streak += 1
        else:
            streak = 0

        if streak == 6:
            containsStreak = True

    if containsStreak:
        numberOfstreaks += 1

    coinFlip = []
    streak = 0
    containsStreak = False

print("Chance of streak: %s%%" % (numberOfstreaks / 100))