from typing import List, Tuple
import time

def two_approx(
    weights: List[int], values: List[int], max_weight: int
) -> Tuple[List[bool], int]:
    assert len(weights) == len(values)
    items_num = len(weights)

    def get_set_and_value_sum(items):
        optimal_set = [0] * items_num
        weight_sum = 0
        for i, _ in sorted(items, key=lambda x: x[1], reverse=True):
            weight_sum += weights[i]
            if weight_sum > max_weight:
                weight_sum -= weights[i]
                break
            optimal_set[i] = values[i]
        values_sum = 0
        for i in range(items_num):
            if optimal_set[i]:
                values_sum += values[i]
        return (values_sum, optimal_set)

    items_greedy = [(i, v / w) for i, (v, w) in enumerate(zip(values, weights))]
    greedy_value, greedy_set = get_set_and_value_sum(items_greedy)
    items_maxgreedy = [(i, v) for i, v in enumerate(values)]
    maxgreedy_value, maxgreedy_set = get_set_and_value_sum(items_maxgreedy)

    best_score = 0
    if greedy_value > maxgreedy_value:
        for i in range(items_num):
            best_score += greedy_set[i]
        return (best_score, greedy_set)
    else:
        for i in range(items_num):
            best_score += maxgreedy_set[i]
        return (best_score, maxgreedy_set)

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

#Посчитаем время работы
start = time.perf_counter()

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
                        best_score, optimal_set = (two_approx(detail_length, detail_length, max_detail_length))
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
            best_score, optimal_set = (two_approx(detail_length, detail_length, max_detail_length))
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

end = time.perf_counter()
print("Время работы алгоритма: ", end-start)