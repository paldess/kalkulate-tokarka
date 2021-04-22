import PySimpleGUI as sg
skor_rez = 180
num = 0
list_result =[]
ustanov = 3
result = 0
sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Токарная обработка:', size=(100, 1), font=("Helvetica", 25))],
            [sg.Text('Наружний диаметр заготовки, мм:', size=(30, 1)), sg.InputText('100', key='-D-')],
            [sg.Text('Конечный диаметр заготовки, мм:', size=(30, 1)), sg.InputText('80', key='-d-')],
            [sg.Text('Скорость резания, м/мин:', size=(30, 1)), sg.Radio('180(сталь)', "RadioDemo", default=True,
                                         size=(15, 1), k='-R180-'),
                                sg.Radio('380(алюминий)', "RadioDemo", default=False, size=(15, 1), k='-R380-')],
            [sg.Text('Длина обрабатываемой части, мм:', size=(30, 1)), sg.InputText('50', key='-dl-')],
            [sg.Text('Наполненность материалом, %:', size=(30, 1)), sg.InputText('100', key='-nap-')],
            [sg.Button('Рассчитать', size=(22, 2)), sg.Button('Добавить расчет', size=(22, 2)),
                            sg.Button('Очистить', size=(22, 2)), sg.Button('Выход', size=(22, 2))],
            [sg.Text('------------', size=(25, 20), key='text1'), sg.Text('------------', size=(48, 20), key='text2'),
                            sg.Text('------------', size=(25, 20), key='text3')]]

# Create the Window
window = sg.Window('Калькулятор времени обработки', layout, size=(800, 500))
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    def ras(D, d, l, p, n):
        skor = p * 1000 / 3.14 / D * 0.2  # скорость обработки в мм/мин
        one_pr = l / skor  # время одного прохода
        return ((D - d) / 3.5 * one_pr) / 100 * n

    if event == sg.WIN_CLOSED or event == 'Выход': # if user closes window or clicks cancel
        break
    if event == 'Очистить':
        window['text1'].update('------------')
        window['text2'].update('------------')
        window['text3'].update('------------')
        result = 0
    if values['-R180-'] == True:
        skor_rez = 180
        # window['text'].update(f'010 {values["-D-"]} = 180')
    elif values['-R380-'] == True:
        skor_rez = 380

    if event == 'Рассчитать':
        # global result
        if not values['-D-'].isdigit() or not values['-d-'].isdigit() or not values['-dl-'].isdigit() or not values['-nap-'].isdigit():
            sg.popup('Внимание!', 'Некорректные данные!')
        elif float(values['-D-']) <= 0 or float(values['-d-']) <= 0 or float(values['-dl-']) <= 0 or float(values['-nap-']) <= 0:
            sg.popup('Внимание!', 'Все значения должны быть больше 0!')
        else:
            num += 1
            D = float(values['-D-'])
            d = float(values['-d-'])
            dl = float(values['-dl-'])
            nap = float(values['-nap-'])
            result = ras(D, d, dl, skor_rez, nap)
            x = str(f' Время обработки этапа:          {round(result, 2)}')
            window['text1'].update(x)

            window['text3'].update('Общее время:               '
                                   'Установка: 2 мин           '
                                   'Замеры: 1 мин              '
                                   f'Обработка: {round(ustanov, 2)}мин')
    if event == 'Добавить расчет':
        if result == 0:
            sg.Popup('Внимание!','Сперва проведите расчеты!')
            continue
        ustanov += result
        list_result.append(result)
        window['text2'].update([f' {i}) ф{D}mm x ф{d}mm x {dl}mm                         '
                                for i, j in enumerate(list_result, 1)])
        window['text3'].update('Общее время:               '
                               'Установка: 2 мин           '
                               'Замеры: 1 мин              '
                               f'Обработка: {round(ustanov, 2)}мин')


window.close()