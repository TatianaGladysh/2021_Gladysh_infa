import turtle

Vx = 2
Vy_0 = 20
Vy = Vy_0
ay = -2
dt = 0.1
x = 0
y = 0
k = 0
turtle.speed(0)
turtle.shape('circle')
turtle.shapesize(0.1, 0.1, 0.01)
for i in range(10000):
    x += Vx * dt
    y += Vy * dt + ay * dt ** 2 / 2
    Vy += ay * dt
    if y < 0:
        Vy = Vy_0 * 0.9
        Vy_0 = Vy_0 * 0.9
    turtle.goto(x, y)
