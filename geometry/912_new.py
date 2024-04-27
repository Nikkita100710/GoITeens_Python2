import matplotlib.pyplot as plt
import numpy as np

# Створюємо площину (сітку) розміром 20x20
plt.figure(figsize=(9, 9))
plt.gcf().canvas.manager.set_window_title('Каданцев   Mикита - Геометрія № 912')
plt.grid(False)
plt.xticks(np.arange(0, 21, 1))
plt.yticks(np.arange(0, 21, 1))

# Встановлення зв'язку між подією натискання клавіші та функцією обробки
def remove_circles(event):
    if event.key == ' ':
        for patch in plt.gca().patches:
            patch.remove()
        plt.draw()
    return True


comment1 = plt.text(3, 13, """
Каданцев   Mикита
Геометрія № 912

""", fontsize=14, color='red', fontweight='bold', fontdict={'family': 'serif', 'style': 'italic'})

comment2 = plt.text(2, 2, """
Дата написання: {9 квітня 2024 року}
Всі права захищені. Уся робота, включаючи програмний код, текст,
графічний дизайн та інші матеріали, які є частиною програми,
є власністю Микити Каданцева, учня 8-го класу загальноосвітньої
закладу "Академічний" у місті Краматорську. 
Програма написана мовою Python з використанням бібліотеки "matplotlib". 
GUI програма оптимізована для запуску на різних операційних системах
без необхідності встановлення Python.
""", fontsize=9, color='black', fontdict={'family': 'serif', 'style': 'italic'})
plt.pause(10)
plt.gcf().canvas.mpl_connect('key_press_event', lambda event: remove_circles(event))
comment1.remove()
comment2.remove()
comment2 = plt.text(2, 10, """
№ 912.

   Центри трьох рівних між собою кіл є вершинами

рівностороннього трикутника. Ці кола не мають спільних точок.

   Скільки існує кіл, які мають зовнішній або внутрішній

 дотик із трьома даними колами?
""", fontsize=11, color='red', fontdict={'family': 'serif', 'style': 'italic'})
plt.pause(15)
comment2.remove()

# Написати коментарі
plt.text(1, 17, """
 Центри трьох рівних між собою кіл є вершинами
рівностороннього трикутника. Ці кола не мають спільних точок
""", fontsize=12, color='blue', fontdict={'family': 'serif', 'style': 'italic'})
plt.pause(2)

# Начальні три круги з вказаними координатами та радіусом 1
circle_centers = [(10.5, 7.6), (8, 12), (13, 12)]
radius = 1
for x, y in circle_centers:
    circle = plt.Circle((x, y), radius, color='blue', fill=False, linewidth=2)
    plt.gca().add_patch(circle)
    plt.pause(2)
plt.pause(2)

# +1 Внутрішнє касаюче коло
plt.text(1, 4, "+1 - Внутрішнє дотичне коло", fontsize=10, color='red')
plt.pause(2)
circle_inner1 = plt.Circle((10.5, 10.5), 1.9, color='red', fill=False)
plt.gca().add_patch(circle_inner1)
plt.pause(3)

# +1 Зовнішнє дотичне коло с диаметром 4
plt.text(1, 3, "+1 - Зовнішнє дотичне коло", fontsize=10, color='red')
plt.pause(2)
circle_inner2 = plt.Circle((10.5, 10.5), 3.95, color='red', fill=False)
plt.gca().add_patch(circle_inner2)
plt.pause(3)

#  Коло навколо одного кола та дотикається двох інших з внутрішньої сторони:
#  3 таких кола, по одному для кожного з трьох початкових кол
plt.text(1, 1, """
+3 - Коло навколо одного кола та дотикається двох інших кіл з внутрішньої
 сторони:  3 таких кола, по одному для кожного з трьох початкових кіл
""", fontsize=10, color='black')
circle_inner1.remove()
plt.pause(0.5)
circle_inner2.remove()
plt.pause(0.5)
circle_inner_1 = plt.Circle((9.36, 11.12), 2.7, color='black', fill=False)
plt.gca().add_patch(circle_inner_1)
plt.pause(1)
circle_inner_2 = plt.Circle((11.64, 11.12), 2.7, color='black', fill=False)
plt.gca().add_patch(circle_inner_2)
plt.pause(1)
circle_inner_3 = plt.Circle((10.5, 9.3), 2.7, color='black', fill=False)
plt.gca().add_patch(circle_inner_3)
plt.pause(5)

# Коло всередині якого два початкових кола і що дотикається третього:
# 3 таких кола, по одному для кожної пари початкових кол.
plt.text(1, -0.2, """
+3 - Коло, всередині якого два початкових кола, і що дотикається третього:
 3 таких кола, по одному для кожної пари початкових кіл
""", fontsize=10, color='green')
circle_inner_1.remove()
plt.pause(0.5)
circle_inner_2.remove()
plt.pause(0.5)
circle_inner_3.remove()
plt.pause(0.5)
circle_inner = plt.Circle((10.5, 12.1), 3.5, color='green', fill=False)
plt.gca().add_patch(circle_inner)
plt.pause(1)
circle_inner = plt.Circle((11.9, 9.7), 3.5, color='green', fill=False)
plt.gca().add_patch(circle_inner)
plt.pause(1)
circle_inner = plt.Circle((9.1, 9.7), 3.5, color='green', fill=False)
plt.gca().add_patch(circle_inner)
plt.pause(5)

comment3 = plt.text(9, 3, """
 Отже, разом у нас є
1 + 1 + 3 + 3 = 8 кіл,
які задовольняють умовам завдання.
""", fontsize=11, color='red', fontdict={'family': 'serif', 'style': 'italic'}, bbox=dict(facecolor='white', edgecolor='red', boxstyle='round,pad=0.5'))
plt.pause(2)
# +1 Внутрішнє касаюче коло
circle_inner1 = plt.Circle((10.5, 10.5), 1.9, color='red', fill=False)
plt.gca().add_patch(circle_inner1)
plt.pause(0.5)
# +1 Зовнішнє дотичне коло с диаметром 4
circle_inner2 = plt.Circle((10.5, 10.5), 3.95, color='red', fill=False)
plt.gca().add_patch(circle_inner2)
plt.pause(2)
#  Коло навколо одного кола та дотикається двох інших з внутрішньої сторони:
#  3 таких кола, по одному для кожного з трьох початкових кол
circle_inner_1 = plt.Circle((9.36, 11.12), 2.7, color='black', fill=False)
plt.gca().add_patch(circle_inner_1)
plt.pause(0.5)
circle_inner_2 = plt.Circle((11.64, 11.12), 2.7, color='black', fill=False)
plt.gca().add_patch(circle_inner_2)
plt.pause(0.5)
circle_inner_3 = plt.Circle((10.5, 9.3), 2.7, color='black', fill=False)
plt.gca().add_patch(circle_inner_3)


plt.pause(5)
plt.gca().set_aspect('equal', adjustable='box')  # Встановимо співвідношення сторін для коректного відображення

# Показуємо графік, не блокуючи виконання програми
plt.show()


