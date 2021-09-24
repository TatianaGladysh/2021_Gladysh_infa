from random import randint
import turtle

number_of_turtles = 10
steps_of_time_number = 10000

pool = [turtle.Turtle(shape='circle') for i in range(number_of_turtles)]
for unit in pool:
    unit.penup()
    unit.speed(0)
    unit.shapesize(2, 2, 1)
    unit.goto(randint(-300, 300), randint(-280, 280))
    unit.right(randint(-180, 180))

for i in range(steps_of_time_number):
    for unit in pool:
        unit.forward(5)
        if unit.xcor() > 300:
            unit.left(2 * (90 - unit.heading()))
            unit.forward(5)
        elif unit.xcor() < -300:
            unit.right(2 * unit.heading()-180)
            unit.forward(5)
        elif unit.ycor() > 280:
            unit.right(2 * unit.heading())
            unit.forward(5)
        elif unit.ycor() < -280:
            unit.right(2 * unit.heading())
            unit.forward(5)
