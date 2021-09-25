import turtle

turtle.shape('turtle')
length = 10
for i in range(1, 21, 1):
    turtle.pendown()
    turtle.forward(i * length)
    turtle.left(90)
    turtle.forward(i * length)
    turtle.left(90)
