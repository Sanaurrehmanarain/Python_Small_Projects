''' 
Given an integer n, representing the height.
Drae a square

Ex) n = 5

X X X X X
X       X
X       X
X       X
X X X X X
'''

def square(n):
	for i in range(0, n):
		if (i == 0 or i == n - 1):
			print("X " * n)
		else:
			print("X " + "   " * (n - 2) + "X")
			
square(5)
  