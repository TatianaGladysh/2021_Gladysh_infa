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


r = 10
t.shape('turtle')
for _ in range(3):
    circle(1, r)
    circle(-1, r)
    t.right(120)
