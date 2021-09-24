import turtle


def print_code(code, x):
    i = 0
    while i < int(len(code)):
        print_type = code[i]
        if print_type == 1:
            turtle.forward(x * code[i + 1])
            i = i + 1
        elif print_type == 2:
            turtle.right(code[i + 1])
            i = i + 1
        elif print_type == 3:
            turtle.left(code[i + 1])
            i = i + 1
        elif print_type == 4:
            turtle.penup()
        elif print_type == 5:
            turtle.pendown()
        i = i + 1


with open("file.txt", "w") as f1:
    f1.write('5 1 1 2 90 1 2 2 90 1 1 2 90 1 2 4 2 90 1 2 \n')
    f1.write('4 2 90 1 1 3 135 5 1 1.414215624 2 135 1 2 4 3 90 1 1 3 90 1 2 2 90 \n')
    f1.write('5 1 1 2 90 1 1 2 45 1 1.414215624 3 135 1 1 4 1 1 3 90 1 2 2 90 \n')
    f1.write('5 1 1 2 135 1 1.414215624 3 135 1 1 2 135 1 1.414215624 4 3 135 1 2 3 90 1 2 2 90 \n')
    f1.write('5 2 90 1 1 3 90 1 1 3 90 1 1 3 180 1 2 3 90 4 1 1 3 90 1 2 2 90 \n')
    f1.write('1 1 2 180 5 1 1 3 90 1 1 3 90 1 1 2 90 1 1 2 90 1 1 4 2 180 1 2 3 90 1 2 2 90 \n')
    f1.write('1 1 2 135 5 1 1.414215624 3 135 1 1 2 90 1 1 2 90 1 1 2 90 1 1 4 2 90 1 2 3 90 1 1 2 90 \n')
    f1.write('5 1 1 2 135 1 1.414215624  3 45 1 1 4 3 90 1 2 3 90 1 2 2 90 \n')
    f1.write('5 1 1 2 90 1 2 2 90 1 1 2 90 1 1 2 90 1 1 2 180 1 1 2 90 1 1 4 2 90 1 2 \n')
    f1.write('5 1 1 2 90 1 1 2 45 1 1.414215624 2 180 1 1.414215624 3  135 1 1 2 90 1 1 4 2 90 1 2')
with open("file.txt", "r") as f:
    s = [0] * 10
    for i in range(10):
        s[i - 1] = f.readline()
    instruction = tuple(s)
index = (1, 4, 1, 7, 0, 0)
# index = (1, 2, 3, 4, 5, 6)
# index = (6, 7, 8, 9, 0, 1)
turtle.penup()
for i in range(len(index)):
    print_code(list(map(float, (instruction[index[i] - 1]).split())), 30)
