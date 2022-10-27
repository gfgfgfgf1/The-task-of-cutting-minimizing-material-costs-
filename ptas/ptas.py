from itertools import chain, combinations

"""PTAS - polynominal time approximation scheme. 
Мы будем использовать PTAS от Sahni(1975).
"""

"""
Жадный поиск
На вход алгоритм принимает
number_of_items (n) - количество предметов
capacity (c) - вместимость рюкзака
prices (p) - цены(ценность) предметов
weights (w) - веса предметов
subset_of_items (M) - подмножество предметов
number_of_operations - количество операций
На выходе алгоритм возвращает
total_value - общая ценность, найденная жадным способом
best_items - предметы, попавшие в лучший набор
"""


def greedy_search(number_of_items, capacity, prices, weights, subset_of_items):
    total_value = 0
    sum_of_weights = 0
    for i in subset_of_items:
        sum_of_weights += weights[i]
    new_capacity = capacity - sum_of_weights
    best_items = set()
    for i in range(number_of_items):
        if i not in subset_of_items and weights[i] <= new_capacity:
            total_value = total_value + prices[i]
            new_capacity = new_capacity - weights[i]
            best_items.add(i)
    return total_value, best_items


"""
Функция subset_of_ndimensional_cube возвращает те множества (1, ..., n), 
размер которых не превышает специальный параметр sahni_parameter.
"""


def subset_of_ndimensional_cube(items, sahni_parameter):
    list_of_items = list(items)
    return list(
        chain.from_iterable(
            combinations(list_of_items, i)
            for i in range(1, min(sahni_parameter + 1, len(list_of_items) + 1))
        )
    )


"""
Аппроксимационная схема Sahni принимает 
number_of_items (n) - количество предметов
capacity (c) - вместимость рюкзака
prices (p) - цены(ценность) предметов
weights (w) - веса предметов
sahni_parameter - специальный параметр
На выходе алгоритм возвращает
total_value - общая ценность, найденная жадным способом
best_items - предметы, попавшие в лучший набор
number_of_operations - количество операций
"""


def sahni(number_of_items, capacity, prices, weights, sahni_parameter):
    total_value = 0
    best_items = set()
    items = [i for i in range(number_of_items)]
    subsets = subset_of_ndimensional_cube(items, sahni_parameter)
    for subset_of_items in subsets:
        sum_of_weights = 0
        for i in subset_of_items:
            sum_of_weights += weights[i]
        if capacity < sum_of_weights:
            continue
        (
            greedy_total_value,
            greedy_best_items,
        ) = greedy_search(number_of_items, capacity, prices, weights, subset_of_items)
        sum_of_prices = 0
        for i in subset_of_items:
            sum_of_prices += prices[i]
        if greedy_total_value + sum_of_prices > total_value:
            total_value = greedy_total_value + sum_of_prices
            best_items = greedy_best_items | set(subset_of_items)
    return total_value, best_items


"""
Polynominal time approximation scheme. 
Алгоритм, как и все другие, принимает 
weights - веса предметов, 
values - ценность предметов,
max_weight - вместимость рюкзака.
"""


def ptas(weights, values, max_weight):
    number_of_items = len(weights)
    total_value, best_items= sahni(
        number_of_items, max_weight, values, weights, 2
    )
    optimal_set = [values[i] if i in best_items else 0 for i in range(len(values))]
    total_weight = 0
    for i in best_items:
        total_weight += weights[i]
    best_score = 0
    for i in range(number_of_items):
        best_score += optimal_set[i]
    return best_score, optimal_set

# размер заготовки(стержня) из которой выпиливаются детали нужного нам размера
# размер заготовки(стержня) не может быть больше размера 5 самых маленьких деталей
max_detail_length = int(input('Введите размер заготовки(стержня), он должен быть кратен 10 и не должен превышать'
                              ' размер 5 самых маленьких деталей\n'))

# размер наименьшей нужной нам детали
smallest_detail = int(input('Введите размер наименьшей детали, он должен быть кратен 10\n'))

# размер наибольшей нужной нам детали
biggest_detail = int(input('Введите размер наибольшей детали, он должен быть кратен 10\n'))

# размер детали, которую не нужно выпиливать из начальной детали
unnecessary_detail = int(input('Введите размер детали, которую выпиливать не нужно, он должен быть кратен 10\n'))

# делаем проверку на то, что пользователь ввел данные правильно
if max_detail_length > 5*smallest_detail or biggest_detail > max_detail_length or max_detail_length % 10 != 0 \
        or smallest_detail % 10 != 0 or biggest_detail % 10 != 0 or unnecessary_detail % 10 != 0:
    # если он ввел их неправильно просим начать сначала
    print('Неправильный ввод, начните сначала и измените входные данные')
# если ввод правильный, то начинаем работу
else:
    # создаем файл, в котором будут лежать все способы раскроя для заданных размеров
    file = open('Cutting_options.txt', 'w')
    file.close()

    # создаем файл, в котором будут лежать все наши решения
    file = open('Program_output.txt', 'w')
    file.close()

    for first_detail in range(smallest_detail, biggest_detail + 10, 10):
        for second_detail in range(smallest_detail, biggest_detail + 10, 10):
            for third_detail in range(smallest_detail, biggest_detail + 10, 10):
                for fourth_detail in range(smallest_detail, biggest_detail + 10, 10):
                    for fifth_detail in range(smallest_detail, biggest_detail + 10, 10):
                        # если есть детали, которые не нужны, то отсекаем их
                        if first_detail == unnecessary_detail or second_detail == unnecessary_detail \
                                or third_detail == unnecessary_detail or fourth_detail == unnecessary_detail \
                                or fifth_detail == biggest_detail:
                            break
                        if fifth_detail == unnecessary_detail:
                            fifth_detail = biggest_detail
                        #создаем список с размером деталей
                        detail_length = [first_detail, second_detail, third_detail, fourth_detail, fifth_detail]
                        # принимаем решение нашей функции
                        #best_score, details = (dynamic_programming(detail_length, max_detail_length))
                        best_score, optimal_set = (ptas(detail_length, detail_length, max_detail_length))
                        # находим значение отходов(брака)
                        wastes = max_detail_length - best_score
                        # сортируем наше решение, чтобы записать его в файл
                        optimal_set.sort()
                        # записываем в файл наше решение, если оно не является 0
                        for j in range(0, 5):
                            file = open('Program_output.txt', 'a')
                            if optimal_set[j] != 0:
                                file.write(str(optimal_set[j]))
                        file.write('\n')
                        file.close()
                        print('Размер заготовки', max_detail_length, '\nПланируемые размеры вырезанной детали:',
                              detail_length, '\nЛучший раскрой:', best_score, '\nКакие детали вырезаны:', optimal_set,
                              '\nОтходы:', wastes)

    # если пользователь хочет вырезать только 1 деталь
    if smallest_detail == biggest_detail:
        if smallest_detail != unnecessary_detail:
            detail_length = [first_detail, second_detail, third_detail, fourth_detail, fifth_detail]
            best_score, optimal_set = (ptas(detail_length, detail_length, max_detail_length))
            wastes = max_detail_length - best_score
            optimal_set.sort()
            for j in range(0, 5):
                file = open('Program_output.txt', 'a')
                if optimal_set[j] != 0:
                    file.write(str(optimal_set[j]))
            file.write('\n')
            file.close()
            print('Максимальный размер детали', max_detail_length, '\nПланируемые размеры вырезанной детали:',
                  detail_length, '\nЛучший раскрой:', best_score, '\nКакие детали вырезаны:', optimal_set,
                  '\nОтходы:', wastes)
        # если эта одна деталь, была указана, как не нужная
        else:
            print('Мы не хотим ничего выпиливать')
    # сортируем файл с нашими решениями(Program_output) для поиска оригинальных решений, их переносим в файл со
    # способами раскроя(Cutting_options)
    with open('Program_output.txt') as sort_file, open('Cutting_options.txt', 'w') as sorting_output:
        sorting_output.write(''.join(set(sort_file)))
    # выводим значения файла со способами раскроя
    print('Способы раскроя для заданных значений:')
    file = open("Cutting_options.txt", "r")
    # считываем все строки
    lines = file.readlines()
    for line in lines:
        print(line.strip())
    file.close