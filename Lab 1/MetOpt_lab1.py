EPS = 1e-9


def pivot(table, basis, r, s):
    #пересчет симплекс-таблицы
    p = table[r][s]
    table[r] = [v / p for v in table[r]]
    for i in range(len(table)):
        if i == r:
            continue
        k = table[i][s]
        table[i] = [table[i][j] - k * table[r][j] for j in range(len(table[i]))]
    basis[r] = s


def simplex(table, basis, allowed):
    #максимизация
    while True:
        #ищем столбец с отрицательной оценкой
        s = None
        for j in allowed:
            if table[-1][j] < -EPS:
                s = j
                break
        if s is None:
            return

        #выбираем выходящую строку
        candidates = []
        for i in range(len(basis)):
            if table[i][s] > EPS:
                candidates.append((table[i][-1] / table[i][s], i))
        if not candidates:
            raise ValueError("задача не ограничена")

        _, r = min(candidates)
        pivot(table, basis, r, s)


def solve(c, A, signs, b):
    m, n = len(b), len(c)

    #если правая часть отрицательна, то умножаем строку на -1
    A = [row[:] for row in A]
    signs = signs[:]
    b = b[:]
    for i in range(m):
        if b[i] < 0:
            b[i] = -b[i]
            A[i] = [-v for v in A[i]]
            if signs[i] == "<=":
                signs[i] = ">="
            elif signs[i] == ">=":
                signs[i] = "<="

    #считаем добавочные и искусственные переменные
    extra = sum(sign != "=" for sign in signs)
    artificial = sum(sign != "<=" for sign in signs)
    total = n + extra + artificial

    #строим расширенную матрицу и начальный базис
    M = [[0.0] * total for _ in range(m)]
    basis = []
    artificial_cols = []
    col = n
    for i in range(m):
        for j in range(n):
            M[i][j] = float(A[i][j])
        if signs[i] == "<=":
            M[i][col] = 1.0              #добавочная переменная
            basis.append(col)
            col += 1
        elif signs[i] == ">=":
            M[i][col] = -1.0             #избыточная переменная
            col += 1
            M[i][col] = 1.0              #искусственная переменная
            basis.append(col)
            artificial_cols.append(col)
            col += 1
        else:                            #равенство
            M[i][col] = 1.0
            basis.append(col)
            artificial_cols.append(col)
            col += 1

    table = [M[i] + [float(b[i])] for i in range(m)]
    table.append([0.0] * (total + 1))

    #максимизируем минус сумму искусственных переменных
    phase1 = [0.0] * total
    for j in artificial_cols:
        phase1[j] = -1.0
    table[-1][:-1] = [-v for v in phase1]
    for i in range(m):
        cb = phase1[basis[i]]
        for j in range(total + 1):
            table[-1][j] += cb * table[i][j]

    simplex(table, basis, range(total))
    if table[-1][-1] < -EPS:
        raise ValueError("система ограничений несовместна")

    #выводим искусственные переменные из базиса
    i = 0
    while i < len(basis):
        if basis[i] in artificial_cols:
            s = None
            for j in range(total):
                if j not in artificial_cols and abs(table[i][j]) > EPS:
                    s = j
                    break
            if s is not None:
                pivot(table, basis, i, s)
                i += 1
            else:
                #избыточное ограничение
                table.pop(i)
                basis.pop(i)
        else:
            i += 1

    #удаляем столбцы искусственных переменных
    keep = [j for j in range(total) if j not in artificial_cols]
    old_to_new = {old: new for new, old in enumerate(keep)}
    table = [[row[j] for j in keep] + [row[-1]] for row in table]
    basis = [old_to_new[j] for j in basis]

    #минимизация c*x через максимизацию -c*x
    cost = [0.0] * len(keep)
    for j in range(n):
        cost[j] = -float(c[j])
    table[-1] = [-v for v in cost] + [0.0]
    for i in range(len(basis)):
        cb = cost[basis[i]]
        for j in range(len(table[-1])):
            table[-1][j] += cb * table[i][j]

    simplex(table, basis, range(len(keep)))

    #читаем значения исходных переменных из базиса
    x = [0.0] * n
    for i in range(len(basis)):
        if basis[i] < n:
            x[basis[i]] = table[i][-1]

    value = sum(c[j] * x[j] for j in range(n))
    return x, value


#данные 4 варианта
c = [3, 1, 4, 2]
A = [
    [2, 1, 1, 0],
    [1, 0, 1, 1],
    [0, 1, 0, 1]
]
signs = ["<=", "=", ">="]
b = [8, 5, 4]

x, z = solve(c, A, signs, b)

print("оптимальная точка:")
for i, value in enumerate(x, 1):
    print(f"x{i} = {value:g}")
print("минимальное значение целевой функции:", f"{z:g}")
