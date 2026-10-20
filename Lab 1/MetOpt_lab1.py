
c = [3, 1, 4, 2]  #z = 3x1 + x2 + 4x3 + 2x4

#ограничения: 
A = [
    [2, 1, 1, 0],
    [1, 0, 1, 1],
    [0, 1, 0, 1]
]
signs = ['<=', '=', '>=']
b = [8, 5, 4]

#создаем пустые строки нужного размера
#переменные: 4 (исходные) + 2 (доп) + 2 (искусственные) + 1 (свободный член) = 9
table = [[0] * 9 for _ in range(4)]

#исходные коэффициенты и правая часть
for i in range(3):
    for j in range(4):
        table[i][j] = A[i][j]
    table[i][8] = b[i]

#добавляем x5 и x6
for i in range(3):
    if signs[i] == '<=':
        table[i][4] = 1
    elif signs[i] == '>=':
        table[i][5] = -1

#добавляем искусственные y1 и y2
table[1][6] = 1 
table[2][7] = 1

#считаем строку W
#переносим все влево: коэффициенты будут с плюсом, свободным членом будет число 9
w_row = [1, 1, 1, 2, 0, -1, 0, 0, 9]
table[3] = w_row

#базис
basis = [4, 6, 7]

print("начальная таблица:")
for row in table:
    print(row)

#разрешающий столбец x4 (индекс 3), разрешающая строка y2 (индекс 2)
pivot_row = 2
pivot_col = 3
pivot_val = table[pivot_row][pivot_col]

#делим разрешающую строку на разрешающий элемент
for j in range(9):
    table[pivot_row][j] = table[pivot_row][j] / pivot_val

#обнуляем остальные элементы в столбце x4
for i in range(4):
    if i != pivot_row:
        factor = table[i][pivot_col]
        for j in range(9):
            table[i][j] = table[i][j] - factor * table[pivot_row][j]

basis[pivot_row] = 3 #теперь в базисе x4

print("\nтаблица после шага 1:")
for row in table:
    print([round(x, 2) for x in row])

#теперь разрешающий столбец x1 (индекс 0), разрешающая строка y1 (индекс 1)
pivot_row = 1
pivot_col = 0
pivot_val = table[pivot_row][pivot_col]

#делим разрешающую строку
for j in range(9):
    table[pivot_row][j] = table[pivot_row][j] / pivot_val

#обнуляем остальные элементы в столбце x1
for i in range(4):
    if i != pivot_row:
        factor = table[i][pivot_col]
        for j in range(9):
            table[i][j] = table[i][j] - factor * table[pivot_row][j]

basis[pivot_row] = 0 #теперь в базисе x1

print("\n решенная вспомогательная задача:")
for row in table:
    print([round(x, 2) for x in row])

# переходим к основной задаче

#так как перед x6 стоит минус, мы можем его увеличивать, чтобы уменьшить z
#берем x6 = 1

x6 = 1
x2 = 0
x3 = 0

#находим остальные переменные
x1 = 1 + x2 - x3 - x6
x4 = 4 - x2 + x6
x5 = 6 - 3*x2 + x3 + 2*x6

#считаем z
z = 3*x1 + x2 + 4*x3 + 2*x4

print("\nответ:")
print("x1 =", x1)
print("x2 =", x2)
print("x3 =", x3)
print("x4 =", x4)
print("z =", z)