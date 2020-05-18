import turtle
joe = turtle.Turtle()
joe.speed(20)

colors = ['red', 'brown', 'green', 'blue']


def sq(a):
    for i in range(3):
        joe.color(colors[i % 4])
        joe.forward(a)
        joe.left(135)


dlina = 10
for i in range(180):
    sq(dlina)
    # joe.circle(dlina)
    joe.right(10)
    dlina += 4