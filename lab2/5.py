import turtle
import numpy as np

turtle.shape('turtle')
length = 10
for i in range(2, 21, 2):
    turtle.pendown()
    turtle.forward(i * length)
    turtle.left(90)
    turtle.forward(i * length)
    turtle.left(90)
    turtle.forward(i * length)
    turtle.left(90)
    turtle.forward(i * length)
    turtle.penup()
    turtle.right(45)
    turtle.forward(np.sqrt(2) * length)
    turtle.left(135)
