from tkinter import *
import time
from Ball import *
window = Tk()

WIDTH = 500
HEIGHT = 500

canvas = Canvas(window, width = WIDTH, height = HEIGHT)
canvas.pack()

soccer_ball1 = Ball(canvas,0, 0, 100, 3, 4, "red")
soccer_ball2 = Ball(canvas,0, 0, 150, 4, 4, "black")
soccer_ball3 = Ball(canvas,0, 0, 120, 2, 1, "blue")
soccer_ball4 = Ball(canvas,0, 0, 180, 1, 6, "yellow")
soccer_ball5 = Ball(canvas,0, 0, 200, 5, 3, "green")

while True:
    soccer_ball1.move()
    soccer_ball2.move()
    soccer_ball3.move()
    soccer_ball4.move()
    soccer_ball5.move()
    window.update()
    time.sleep(0.02)
window.mainloop()