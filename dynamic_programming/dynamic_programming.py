# все размеры должны быть кратны 10
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
    # создаем функцию dynamic_programming для решения задачи о рюкзаке методами динамического программирования
    # в функцию задаем длину требуемых деталей(detail_length) и максимальный размер заготовки(max_detail_length)
    # в функции используется таблица мемоизации, в ее ячейках будут храниться результаты вычислений, что позволит
    # быстро найти оптимальное решение
    def dynamic_programming(detail_length, max_detail_length):
        n = len(detail_length)  # находим размер таблицы
        table = [[0 for x in range(max_detail_length + 1)] for x in range(n + 1)]  # создаём таблицу из нулевых значений

        for i in range(n + 1):
            for j in range(max_detail_length + 1):
                # базовый случай
                if i == 0 or j == 0:
                    table[i][j] = 0
                # если площадь предмета меньше площади столбца,
                # максимизируем значение суммарной ценности(или веса, в нашем случае это не имеет значения)
                elif detail_length[i - 1] <= j:
                    table[i][j] = max(detail_length[i - 1]
                                      + table[i - 1][j - detail_length[i - 1]], table[i - 1][j])
                # если площадь предмета больше площади столбца,
                # забираем значение ячейки из предыдущей строки
                else:
                    table[i][j] = table[i - 1][j]
        details = [0 for i in range(n)]  # создаем список деталей, которые будем выпиливать из заготовки
        # функция, которая выводит какие детали будут выпилены из заготовки
        # задаем функции размер нашей таблицы и размер заготовки
        def which_length(last_details, detail_length_of_kit):
            # значение ячейки таблицы 0, то ничего не делаем
            if table[last_details][detail_length_of_kit] == 0:
                return
            # если значение предыдущей ячейки таблицы равно значению текущей,
            # то запускаем нашу функцию с измененным размером
            if table[last_details - 1][detail_length_of_kit] == table[last_details][detail_length_of_kit]:
                which_length(last_details - 1, detail_length_of_kit)
            else:
                # снова перезапускаем функцию, чтобы пройти по всем ячейкам таблицы
                which_length(last_details - 1, detail_length_of_kit - detail_length[last_details - 1])
                # массив деталей, которые берём (по стандарту 0)
                details[last_details - 1] = detail_length[last_details - 1]

        which_length(n, max_detail_length)
        # основная функция возвращает лучшее решение нашей задачи и какие детали будут вырезаны
        return table[n][max_detail_length], details

    # создаем файл, в котором будут лежать все способы раскроя для заданных размеров
    file = open('Cutting_options.txt', 'w')
    file.close()

    # создаем файл, в котором будут лежать все наши решения
    file = open('Program_output.txt', 'w')
    file.close()

    # пробегаемся по всем деталям, для нахождения решения
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
                        # создаем список с размером деталей
                        detail_length = [first_detail, second_detail, third_detail, fourth_detail, fifth_detail]
                        # принимаем решение нашей функции
                        best_score, details = (dynamic_programming(detail_length, max_detail_length))
                        # находим значение отходов(брака)
                        wastes = max_detail_length - best_score
                        # сортируем наше решение, чтобы записать его в файл
                        details.sort()
                        # записываем в файл наше решение, если оно не является 0
                        for j in range(0, 5):
                            file = open('Program_output.txt', 'a')
                            if details[j] != 0:
                                file.write(str(details[j]))
                        file.write('\n')
                        file.close()
                        # выводим ответы для всех наших решений
                        print('Размер заготовки', max_detail_length, '\nРазмер вырезанной детали:',
                              detail_length, '\nЛучший раскрой:', best_score, '\nКакие детали вырезаны:', details,
                              '\nОтходы:', wastes)
    # если пользователь хочет вырезать только 1 деталь
    if smallest_detail == biggest_detail:
        if smallest_detail != unnecessary_detail:
            detail_length = [first_detail, second_detail, third_detail, fourth_detail, fifth_detail]
            best_score, details = (dynamic_programming(detail_length, max_detail_length))
            wastes = max_detail_length - best_score
            details.sort()
            for j in range(0, 5):
                file = open('Program_output.txt', 'a')
                if details[j] != 0:
                    file.write(str(details[j]))
            file.write('\n')
            file.close()
            print('Максимальный размер детали', max_detail_length, '\nРазмер вырезанной детали:',
                  detail_length, '\nЛучший раскрой:', best_score, '\nКакие детали вырезаны:', details,
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