import random

messages = ["It is certain",
    "It is decidedly so",
    "Yes definitely",
    "Reply hazy try again",
    "Ask again later",
    "Concentrate and ask again",
    "My reply is no",
    "Outlook not so good",
    "Very doubtful"]

# method one to print out random output

#print(messages[random.randint(0, len(messages) -1)])

# methid two to print out random output

print(random.choice(messages))


