import math

def calc_cosh(x, eps):
    if eps <= 0:
        print("eps должно быть больше 0")
        return None

    # Начальные значения
    N = 1
    term = 1.0   # первое слагаемое (x^0 / 0! = 1)
    s = term
    expt = (math.exp(x) + math.exp(-x)) / 2
    diff = abs(s - expt)

    # Итерации
    while diff > eps:
        term *= x * x / ((2 * N - 1) * (2 * N))  # рекуррентное вычисление нового слагаемого
        s += term
        N += 1
        diff = abs(s - expt)

    return s, N, diff

# Пример
x = float(input("Введите x: "))
eps = float(input("Введите eps: "))

result = calc_cosh(x, eps)
if result:
    approx, terms, diff = result
    print(f"Приближенное значение cosh(x): {approx}")
    print(f"Количество членов ряда: {terms}")
    print(f"Погрешность: {diff}")
    print(f"Точное значение (math.cosh): {math.cosh(x)}")
