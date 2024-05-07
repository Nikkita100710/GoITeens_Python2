import asyncio
import time
from datetime import datetime

# Функція для отримання поточного часу з точністю до мілісекунд
def current_time():
    current = time.time()
    millis = int((current - int(current)) * 1000)
    return datetime.now().strftime("%H:%M:%S") + f".{millis:03d}"

# Асинхронна функція, яка представляє собою завдання, що спить на певний час
async def task(name, seconds):
    start_time = current_time()  # Фіксуємо час початку виконання завдання з точністю до мілісекунд
    print(f"{name} почав виконання о {start_time}")
    await asyncio.sleep(seconds)  # Чекаємо задану кількість секунд
    end_time = current_time()  # Фіксуємо час закінчення виконання завдання з точністю до мілісекунд
    start_time_obj = datetime.strptime(start_time, "%H:%M:%S.%f")
    end_time_obj = datetime.strptime(end_time, "%H:%M:%S.%f")
    time_diff = end_time_obj - start_time_obj
    print(f"{name} завершив виконання о {end_time}. Час виконання: {time_diff.total_seconds()} с")

# Асинхронна функція, що виконує головну програму
async def main():
    print("Початок програми")
    await asyncio.gather(
        task("Завдання 1", 2),
        task("Завдання 2", 1),
        task("Завдання 3", 3)
    )
    print("Програма завершилася")

asyncio.run(main())
