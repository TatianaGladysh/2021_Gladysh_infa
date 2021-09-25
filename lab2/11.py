import turtle as t


def circle(side, length):
    n = 50
    angle = (n - 2) * 180 / n
    if side == 1:
        for _ in range(0, n, 1):
            t.forward(length)
            t.left(180 - angle)
    else:
        for _ in range(0, n, 1):
            t.forward(length)
            t.right(180 - angle)


r = 2
dr = 0.5
t.shape('turtle')
t.right(90)
for i in range(1, 11):
    circle(1, dr * i + r)
    circle(-1, dr * i + r)
