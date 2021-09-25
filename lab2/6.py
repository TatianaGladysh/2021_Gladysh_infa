import turtle as t

t.shape("turtle")
t.pendown()

n = int(input())
angle = 360 / n
length = 100

for _ in range(n):
    t.forward(length)
    t.stamp()
    t.right(180)
    t.forward(length)
    t.right(180 - angle)
