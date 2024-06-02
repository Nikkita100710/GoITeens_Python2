import matplotlib.pyplot as plt
import numpy as np

# Створюємо площину (сітку) розміром 20x20
plt.figure(figsize=(8, 8))
plt.grid(False)
plt.xticks(np.arange(0, 21, 1))
plt.yticks(np.arange(0, 21, 1))

comment1 = plt.text(5, 10, """
Каданцев   Mикита

Геометрія № 912
""", fontsize=15, color='red', fontdict={'family': 'serif', 'style': 'italic'})
plt.pause(5)
comment1.remove()

comment2 = plt.text(2, 11, """
№ 912.

   Центри трьох рівних між собою кіл є вершинами

рівностороннього трикутника. Ці кола не мають спільних точок.

   Скільки існує кіл, які мають зовнішній або внутрішній

 дотик із трьома даними колами?
""", fontsize=11, color='red', fontdict={'family': 'serif', 'style': 'italic'})
plt.pause(15)
comment2.remove()

# Написати коментарі
plt.text(1, 17.5, """
 Центри трьох рівних між собою кіл є вершинами
рівностороннього трикутника. Ці кола не мають спільних точок
""", fontsize=12, color='blue')
plt.pause(1)
# plt.text(5, 14, "(комментарий 1)", fontsize=10, color='gray')

# Начальні три круги з вказаними координатами та радіусом 1
circle_centers = [(10.5, 7.6), (8, 12), (13, 12)]
radius = 1
for x, y in circle_centers:
    circle = plt.Circle((x, y), radius, color='blue', fill=True)
    plt.gca().add_patch(circle)
    plt.pause(1)

center_x = sum([center[0] for center in circle_centers]) / len(circle_centers)
center_y = sum([center[1] for center in circle_centers]) / len(circle_centers)
plt.pause(4)

# +1 Внутрішнє касаюче коло
plt.text(1, 4, "+1 - Внутрішнє дотичне коло", fontsize=10, color='red')
plt.pause(1)
circle_inner = plt.Circle((10.5, 10.5), 1.9, color='red', fill=False)
plt.gca().add_patch(circle_inner)
plt.pause(4)
# +1 Зовнішнє дотичне коло с диаметром 4
plt.text(1, 3, "+1 - Зовнішнє дотичне коло", fontsize=10, color='red')
plt.pause(1)
circle_inner = plt.Circle((10.5, 10.5), 3.95, color='red', fill=False)
plt.gca().add_patch(circle_inner)
plt.pause(4)

#  Коло навколо одного кола та дотикається двох інших з внутрішньої сторони:
#  3 таких кола, по одному для кожного з трьох початкових кол

plt.text(1, 1, """
+3 - Коло навколо одного кола та дотикається двох інших кіл з внутрішньої
 сторони:  3 таких кола, по одному для кожного з трьох початкових кіл
""", fontsize=10, color='black')
plt.pause(1)
circle_inner = plt.Circle((9.36, 11.12), 2.7, color='black', fill=False)
plt.gca().add_patch(circle_inner)
plt.pause(1)
circle_inner = plt.Circle((11.64, 11.12), 2.7, color='black', fill=False)
plt.gca().add_patch(circle_inner)
plt.pause(1)
circle_inner = plt.Circle((10.5, 9.3), 2.7, color='black', fill=False)
plt.gca().add_patch(circle_inner)
plt.pause(8)


# Коло всередині якого два початкових кола і що дотикається третього:
# 3 таких кола, по одному для кожної пари початкових кол.
plt.text(1, 0, """
+3 - Коло, всередині якого два початкових кола, і що дотикається третього:
 3 таких кола, по одному для кожної пари початкових кіл
""", fontsize=10, color='green')
plt.pause(1)

circle_inner = plt.Circle((10.5, 12.1), 3.5, color='green', fill=False)
plt.gca().add_patch(circle_inner)
plt.pause(1)
circle_inner = plt.Circle((11.9, 9.7), 3.5, color='green', fill=False)
plt.gca().add_patch(circle_inner)
plt.pause(1)
circle_inner = plt.Circle((9.1, 9.7), 3.5, color='green', fill=False)
plt.gca().add_patch(circle_inner)
plt.pause(8)

comment3 = plt.text(9, 2, """
 Отже, разом у нас є
1 + 1 + 3 + 3 = 8 кіл,
які задовольняють умовам завдання.
""", fontsize=12, color='red', fontdict={'family': 'serif', 'style': 'italic'})
plt.pause(5)

plt.gca().set_aspect('equal', adjustable='box')  # Встановимо співвідношення сторін для коректного відображення
plt.show()
