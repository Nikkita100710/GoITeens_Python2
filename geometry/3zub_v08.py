import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Координати частин
points_parts = [
    [(0, 9), (1, 8), (0.5, 2), (2, -1), (3, 0), (2, 1), (2.5, 5.5), (5, 8), (5, -4),
     (2, -4), (1, -6), (0, -7)],
    [(0, 9), (-1, 8), (-0.5, 2), (-2, -1), (-3, 0), (-2, 1), (-2.5, 5.5), (-5, 8),
     (-5, -4), (-2, -4), (-1, -6), (0, -7)],
    [(4, -0.5), (4, -3), (2.5, -3), (2, -2), (4, -0.5)],
    [(-4, -0.5), (-4, -3), (-2.5, -3), (-2, -2), (-4, -0.5)],
    [(4, 0), (4, 5.5), (3.5, 5), (3, 1), (4, 0)],
    [(-4, 0), (-4, 5.5), (-3.5, 5), (-3, 1), (-4, 0)],
    [(1, -2), (1.5, -3), (0.5, -3), (1, -2)],
    [(-1, -2), (-1.5, -3), (-0.5, -3), (-1, -2)],
    [(-0.5, -4), (-1, -4), (-0.5, -5.5), (-0.5, -4)],
    [(0.5, -4), (1, -4), (0.5, -5.5), (0.5, -4)],
    [(0, 1), (-1, -1), (0, -2)],
    [(0, 1), (1, -1), (0, -2)]
]

# Налаштування анімації
total_duration = 10000  # Загальна тривалість анімації в мілісекундах (10 секунд)
total_points = 0
for i in range(0, len(points_parts), 2):
    total_points += max(len(points_parts[i]), len(points_parts[i + 1]))

interval = total_duration // total_points  # Інтервал анімації
pause_duration = 500  # Продовження паузи перед повтором у мілісекундах

# Створення графіка
fig, ax = plt.subplots(figsize=(10, 10))  # Збільшення розміру вікна

# Встановлення кольору фону
ax.set_facecolor('#2255aa')  # Темно-синій колір

# Налаштування осей
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_aspect('equal', adjustable='box')

# Додавання підпису під графіком
fig.text(0.5, 0.05, 'Анімація створена за допомогою бібліотеки Matplotlib та FFmpeg '
                    '(Микита Каданцев, Python 3.12)',
         ha='center', fontsize=12, color='blue')

# Жовті лінії для кожної частини
lines = [ax.plot([], [], color='#FFD700', lw=4)[0] for _ in points_parts]

# Рамка
for spine in ax.spines.values():
    spine.set_edgecolor('yellow')
    spine.set_linewidth(2)


def init():
    for line in lines:
        line.set_data([], [])
    return lines


def update(frame):
    # Оновлення індексу для повторення анімації після паузи
    actual_frame = frame % (total_points + (pause_duration // interval))

    # Якщо це кадр під час паузи, не оновлюємо
    if actual_frame >= total_points:
        return lines

    # Прорисовка
    accumulated_frames = 0
    for i in range(0, len(points_parts), 2):
        part_len = max(len(points_parts[i]), len(points_parts[i + 1]))
        if accumulated_frames + part_len > actual_frame:
            part_frame = actual_frame - accumulated_frames

            x_data_1 = [p[0] for p in points_parts[i][:min(part_frame + 1, len(points_parts[i]))]]
            y_data_1 = [p[1] for p in points_parts[i][:min(part_frame + 1, len(points_parts[i]))]]

            x_data_2 = [p[0] for p in points_parts[i + 1][:min(part_frame + 1, len(points_parts[i + 1]))]]
            y_data_2 = [p[1] for p in points_parts[i + 1][:min(part_frame + 1, len(points_parts[i + 1]))]]

            if part_frame >= len(points_parts[i]):
                x_data_1 += [points_parts[i][-1][0]] * (part_frame + 1 - len(points_parts[i]))
                y_data_1 += [points_parts[i][-1][1]] * (part_frame + 1 - len(points_parts[i]))

            if part_frame >= len(points_parts[i + 1]):
                x_data_2 += [points_parts[i + 1][-1][0]] * (part_frame + 1 - len(points_parts[i + 1]))
                y_data_2 += [points_parts[i + 1][-1][1]] * (part_frame + 1 - len(points_parts[i + 1]))

            lines[i].set_data(x_data_1, y_data_1)
            lines[i + 1].set_data(x_data_2, y_data_2)
            break
        accumulated_frames += part_len

    return lines


# Створення анімації
ani = FuncAnimation(fig, update, frames=total_points + (pause_duration // interval),
                    init_func=init, blit=True, interval=interval, repeat=True)

# Збереження анімації у файл
ani.save('Ukrainian_trident_b.gif', writer='pillow', fps=1000 // interval)
ani.save('Ukrainian_trident_b.mp4', writer='ffmpeg', fps=1000 // interval)

# Відображення графіка
plt.show()


