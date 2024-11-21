suma = int(input("Введіть число n (1 ≤ n ≤ 10^6): "))
banknotes = (500, 200, 100, 50, 20, 10)
amount = 0
if suma % 10 != 0:
    print(-1)
else:
    for i in banknotes:
        if suma == 0:  # Якщо сума вже видана
            break
        if suma >= i:
            amount += suma // i  # Додаємо купюри
            suma %= i  # Оновлюємо залишок
    print(amount)
