import csv
import operator


def csv_file(link: str):
    """считываем csv file и сохраняем его в список для дальнейшей обработки.
    Функция ловит исключение при вводе неправильных ссылок"""
    dataset = []
    try:
        with open(link, newline='') as csvfile:
            file = csv.DictReader(csvfile, delimiter=';')
            for i in file:
                dataset.append(i)
    except FileNotFoundError:
        print('Проверьте ссылки')
    return dataset


def all_data(dataset: list):
    """Функция возвращает список из иерархии и сводным отчетом по департаментам"""
    dict_teams = {}
    dict_dep = {}
    k = 0
    department_data = []
    for i in dataset:
        data = [0] * 6
        if i['Отдел'] not in dict_teams.keys():
            dict_teams[i['Отдел']] = i['Департамент']   # создаем словарь с ключами по отделам
        if i['Департамент'] not in dict_dep.keys():
            dict_dep[i['Департамент']] = k
            k += 1
            data[0] = i['Департамент']
            data[1] = 1
            data[2] = int(i['Оклад'])
            data[3] = int(i['Оклад'])
            data[4] = int(i['Оклад'])
            data[5] = round(float(data[4]) / data[1], 2)
            department_data.append(data)
        else:
            data = department_data[dict_dep[i['Департамент']]]
            data[1] += 1
            if data[2] > int(i['Оклад']):
                data[2] = int(i['Оклад'])   # минимальный оклад
            if data[3] < int(i['Оклад']):
                data[3] = int(i['Оклад'])   # максимальный оклад
            data[4] += int(i['Оклад'])   # сумма окладов, которая не нужна в итоге
            data[5] = round(float(data[4]) / data[1], 2)   # средний оклад
    sorted_teams = sorted(dict_teams.items(), key=operator.itemgetter(1))
    sorted_dict = {k: v for k, v in sorted_teams}
    return [sorted_dict, department_data]


def print_dep_structure(sorted_dict: dict):
    """функция печатает возвращенное функцией all_data значение
    sorted_dict (отдел - департамент) в виде иерархии"""
    m = ''
    for k, v in sorted_dict.items():
        if v == m:
            print(k, end='\t')
        elif m == '':
            print('{}:'.format(v))
            print(k,  end='\t')
            m = v
        else:
            print()
            print('__________________')
            print('{}:'.format(v))
            print(k, end='\t')
            m = v
    print()
    return 0


def print_report(department_data: list):
    """функция печатает возвращенное функцией all_data значение department_data в виде отчета"""
    space = 17
    head1 = 'Департамент'
    sp1 = ' ' * (space - len(head1))
    print('{0}{1}'.format(head1, sp1), end='\t')
    head2 = 'Кол-во сотрудников'
    sp2 = ' ' * (space - len(head2))
    print('{0}{1}'.format(head2, sp2), end='\t')
    head3 = 'Мин. оклад'
    sp3 = ' ' * (space - len(head3))
    print('{0}{1}'.format(head3, sp3), end='\t')
    head4 = 'Макс. оклад'
    sp4 = ' ' * (space - len(head4))
    print('{0}{1}'.format(head4, sp4), end='\t')
    head5 = 'Средний оклад'
    sp5 = ' ' * (space - len(head5))
    print('{0}{1}'.format(head5, sp5))

    for i in department_data:
        k = 0
        for j in i:
            if k == 4:
                k += 1
            else:
                space1 = ' ' * (space - len(str(j)))
                print(j, space1, end='\t')
                k += 1
        print()
    return 0


def save_report(link: str, link2: str):
    """функция сохраняет отчет department_data в файл, путь к которому предоставил пользователь"""
    dataset = csv_file(link)
    data = all_data(dataset)
    for_save = data[1]
    file = open(link2, 'w')
    header = (
        'Департамент',
        'Кол-во сотрудников',
        'Мин. оклад',
        'Макс. оклад',
        'Средний оклад')
    with file as f:
            w = csv.writer(f, delimiter=';')
            w.writerow(header)
            for i in for_save:
                line_to_write = []
                k = 0
                for j in i:
                    if k == 4:
                        k += 1
                    else:
                        line_to_write.append(j)
                        k += 1
                w.writerow(line_to_write)


def ask_user(link: str, link2: str):
    """функция спрашивает пользователя, какая информация ему требуется и предоставляет ее"""
    option = 0
    options = {1: 'Вывести иерархию команд', 2: 'Вывести сводный отчет', 3: 'Сохранить сводный отчет'}
    for k, v in options.items():
        print(f'{k} - {v}')
    while option not in options:
        print("Выберите действие: 1: 'Вывести иерархию команд', 2: 'Вывести сводный отчет', 3: 'Сохранить сводный отчет")
        option = int(input())
    data = all_data(csv_file(link))
    if option == 1:
        print_dep_structure(data[0])
    elif option == 2:
        print_report(data[1])
    elif option == 3:
        save_report(link, link2)
    else:
        return 0


print('Введите название/путь исходного файла: ')
link = input()
print('Введите название файла, куда сохранить отчет: ')
link2 = input()
ask_user(link, link2)
