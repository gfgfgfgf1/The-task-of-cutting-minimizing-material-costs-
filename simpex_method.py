from pulp import LpMinimize, LpProblem, LpStatus, lpSum, LpVariable
# Определяем модель
model = LpProblem(sense=LpMinimize)

# Описываем переменные
x = {i: LpVariable(name=f"x{i}", lowBound=0) for i in range(1, 8)}

# Добавляем ограничения
model += (lpSum(x.values()) <= 50, "ответ не может превышать 50 м ")
model += (5 * x[1] + 3 * x[2] + 2 * x[3] + 2 * x[4] + x[5] >= 95, "ограничение на деталь размером 20 см")
model += (x[2] + 2 * x[3] + x[5] + 3 * x[6] >= 45, "ограничение на деталь размером 30 см")
model += (x[4] + x[5] + 2 * x[7] >= 35, "ограничение на деталь размером 50 см")

# Описываем цель
# Так как минимизация, то все значения с -
model += - x[1] - x[2] - x[3] - x[4] - x[5] - x[6] - x[7]

# Решаем задачу оптимизации
status = model.solve()

# Выводим результаты решения
print(f"status: {model.status}, {LpStatus[model.status]}")
print(f"objective: {model.objective.value()}")

for var in x.values():
    print(f"{var.name}: {var.value()}")

for name, constraint in model.constraints.items():
    print(f"{name}: {constraint.value()}")