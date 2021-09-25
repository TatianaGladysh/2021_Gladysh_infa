import turtle

turtle.shape('turtle')
turtle.speed(0)
for i in range(50, 1000, 1):
    turtle.forward(1)
    angle = (i - 2) * 180 / i
    turtle.left((180 - angle))
