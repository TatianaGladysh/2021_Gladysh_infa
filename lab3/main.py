from random import randint
import turtle

turtle.speed(0)
turtle.shape('turtle')
for i in range(1000):
    turtle.forward(randint(1, 50))
    if randint(1, 2) % 2 == 0:
        turtle.left(randint(0, 180))
    else:
        turtle.right(randint(0, 180))
