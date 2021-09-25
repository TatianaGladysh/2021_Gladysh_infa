import turtle
import numpy as np


def polygon(n, r):
    side = 2 * r * np.sin(np.pi / n)
    angle = 360 / n
    for _ in range(n):
        turtle.left(angle/2)
        turtle.forward(side)
        turtle.left(angle/2)
    turtle.right(90)


turtle.shape('turtle')
k = 10
for i in range(1, 11):
    polygon(i+2, k*i)
    turtle.penup()
    turtle.forward(k)
    turtle.left(90)
    turtle.pendown()
