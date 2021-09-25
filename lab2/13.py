import turtle as t


def circle(side, length):
    n = 100
    angle = (n - 2) * 180 / n
    if side == 1:
        for _ in range(0, n, 1):
            t.left((180 - angle) / 2)
            t.forward(length)
            t.left((180 - angle) / 2)
    else:
        for _ in range(0, n, 1):
            t.right((180 - angle) / 2)
            t.forward(length)
            t.right((180 - angle) / 2)


def semicircle(side, length):
    n = 100
    angle = (n - 2) * 180 / n
    if side == 1:
        for _ in range(0, n // 2, 1):
            t.forward(length)
            t.left(180 - angle)
    else:
        for _ in range(0, n // 2, 1):
            t.forward(length)
            t.right(180 - angle)


t.shape('turtle')
big_length = 7
small_length = 1.75
smile_length = 3.1
t.fillcolor('yellow')
# t.color( 'black', 'black')
t.begin_fill()
circle(1, big_length)
t.end_fill()
t.left(90)
t.penup()
t.forward(130)
t.right(90)
t.forward(50)
t.pendown()
t.fillcolor('blue')
t.begin_fill()
circle(1, small_length)
t.end_fill()
t.left(180)
t.penup()
t.forward(100)
t.pendown()
t.fillcolor('blue')
t.begin_fill()
circle(-1, small_length)
t.end_fill()
t.penup()
t.left(90)
t.forward(50)
t.pendown()
t.color('red')
t.width(10)
semicircle(1, smile_length)
t.penup()
t.left(90)
t.forward(50)
t.right(90)
t.pendown()
t.color('black')
t.width(10)
t.forward(50)
# input()
