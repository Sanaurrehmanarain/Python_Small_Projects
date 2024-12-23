cat_names = []
while True:
    print("Enter the name of cat" + str(len(cat_names) + 1) + " (Or enter nothing to stop.):")
    name = input()
    if name == "":
        break
    cat_names = cat_names + [name]   # list concatenation
print("The cat name are:")
for name in cat_names:   # we use for loop with a list i.e. cat_names
    print(" " + name)
