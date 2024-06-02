import turtle

# Створення екрану
canvas = turtle.Screen()
canvas.setup(width=1280, height=720)  # Встановлення роздільної здатності екрану 16:9
canvas.bgcolor("lightgray")
canvas.title("Микита Каданцев")

# Створення черепахи
yungMula = turtle.Turtle()
yungMula.speed(0)
yungMula.pencolor("red")

# Переміщення черепахи в центр
yungMula.penup()
yungMula.goto(0, 0)
yungMula.pendown()

# Малювання
scale = 0.4  # Масштабування, щоб рисунок помістився в межах екрану
for x in range(1000):
    yungMula.forward(x * scale)
    yungMula.left(200)
    yungMula.circle(x * scale)

# Залишення вікна з графікою відкритим
turtle.done()


