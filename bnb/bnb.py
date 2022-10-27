from typing import List, Tuple


def bnb(
    weights: List[int], values: List[int], max_weight: int
) -> Tuple[List[bool], int]:
    assert len(weights) == len(values)

    items_num = len(weights)
    items_value_density = [(i, v / w) for i, (v, w) in enumerate(zip(values, weights))]
    items_value_density.sort(key=lambda x: x[1], reverse=True)


    max_lower_bound = 0
    best_skip_set = set()
    best_force_set = set()
    queue = [(set(), set())]

    while len(queue) > 0:
        (force_items, skip_items) = queue.pop()
        upper_bound = 0
        lower_bound = 0
        weight_sum = 0

        for i in force_items:
            weight_sum += weights[i]
            lower_bound += values[i]
        if weight_sum > max_weight:
            continue
        if len(force_items) + len(skip_items) == items_num:
            if lower_bound >= max_lower_bound:
                max_lower_bound = lower_bound
                best_skip_set = skip_items
                best_force_set = force_items
            continue

        upper_bound = lower_bound
        last_item = None
        for i, _ in items_value_density:
            if i in skip_items or i in force_items:
                continue
            last_item = i
            new_weight = weights[i] + weight_sum
            if new_weight >= max_weight:
                item_fraction = (max_weight - weight_sum) / weights[i]
                upper_bound += item_fraction * values[i]
                break
            weight_sum = new_weight
            upper_bound += values[i]

        if upper_bound < max_lower_bound:
            continue

        if lower_bound > max_lower_bound:
            max_lower_bound = lower_bound

        skip_items_copy = skip_items.copy()
        skip_items_copy.add(last_item)
        right_branch = (force_items, skip_items_copy)
        queue.append(right_branch)
        force_items_copy = force_items.copy()
        force_items_copy.add(last_item)
        left_branch = (force_items_copy, skip_items)
        queue.append(left_branch)

    optimal_set = [
        values[i] if i in best_force_set or i not in best_skip_set else 0
        for i in range(items_num)
    ]
    best_score = 0
    for i in range(items_num):
        best_score += optimal_set[i]
    return (best_score, optimal_set)

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
                        best_score, optimal_set = (bnb(detail_length, detail_length, max_detail_length))
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
            best_score, optimal_set = (bnb(detail_length, detail_length, max_detail_length))
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