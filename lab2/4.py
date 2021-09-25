import turtle

n = 100
angle = (n - 2) * 180 / n
turtle.shape('turtle')
for _ in range(0, n, 1):
    turtle.forward(5)
    turtle.left(180 - angle)
