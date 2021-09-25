import turtle


def star(n):
    an = (n - 1) * 180 / n
    for _ in range(0, n, 1):
        turtle.forward(75)
        turtle.left(an)


turtle.shape('turtle')
star(5)
turtle.penup()
turtle.forward(150)
turtle.pendown()
star(11)
