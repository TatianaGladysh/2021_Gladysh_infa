import turtle as t


def semicircle(side, length):
    n = 100
    angle = (n - 2) * 180 / n
    if side == 1:
        for _ in range(0, n // 2, 1):
            t.left((180 - angle) / 2)
            t.forward(length)
            t.left((180 - angle) / 2)
    else:
        for _ in range(0, n // 2, 1):
            t.right((180 - angle) / 2)
            t.forward(length)
            t.right((180 - angle) / 2)


r = 0.7
R = 2
t.shape('turtle')
t.left(90)
for _ in range(5):
    semicircle(1, R)
    semicircle(1, r)
