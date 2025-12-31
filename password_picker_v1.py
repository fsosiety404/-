'''импортируем все нужные библиотеки'''
import random
import time
import pyautogui
import pyperclip
from tkinter import *
from pynput.mouse import Controller

'''делаем глобальные переменные'''
global_x_text = 0
global_y_text = 0
global_x_btn = 0
global_y_btn = 0
global runn

'''сщздаём пустую функцию для остановки'''
def stop_go_btn():
    return

'''создаём функцию для горячей клавиши'''
def stop_hotkey(event):
    runn = False
    btn_go.config(command=stop_go_btn)

def go_passw(x, y, perv_num, x_btn, y_btn):
    runn = True
    while True:
        '''создаём список из всех символов'''
        test_sp = ['1','2','3','4','5','6','7','8','9','0', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', 'q', 'w', 'e', 't', 'y', 'u', 'i', 'o', ' ', '[', ']', 'a','s', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ':', ';', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.' ,'/', '|']

        '''создаём переменную в которой будет хранится рандомное число'''
        num_rn = random.randint(0, 10)
        '''создаём пароль'''
        password_otv1 = random.sample(test_sp, num_rn)
        password_otv2 = ''.join(password_otv1)
        password_otv3 = f'{perv_num}{password_otv2}'

        '''копируем наш текст'''
        pyperclip.copy(password_otv3)

        '''кликаем по окошку где надо вводить текст'''
        pyautogui.click(x=x, y=y)
        time.sleep(0.1)

        '''вставляем наш пароль'''
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.08)

        '''кликаем по кнопке для проверки текста'''
        pyautogui.click(x=x_btn, y=y_btn)
        time.sleep(0.1)

        '''кликаем обратно в поле ввода'''
        pyautogui.click(x=x, y=y)
        time.sleep(0.1)

        '''очищаем поле'''
        for i in range(15):
            pyautogui.hotkey('Backspace')

        if not runn:
            break

def scan_poz():
    global global_x_text, global_y_text
    mouse = Controller()
    time.sleep(3)
    '''определяем координаты'''
    x_coor, y_coor = mouse.position
    '''выводим на окно'''
    lb_text_coor.config(text=f'x={x_coor}, y={y_coor}')
    '''сохраняем в глобальные переменные'''
    global_x_text = x_coor
    global_y_text = y_coor

def scan_poz_btn():
    global global_x_btn, global_y_btn
    poz = Controller()
    time.sleep(3)
    '''определяем координаты'''
    x_coor_btn, y_coor_btn = poz.position
    '''выводим на окно'''
    lb_btn_coor.config(text=f'x={x_coor_btn}, y={y_coor_btn}')
    '''сохраняем в глобальные переменные'''
    global_x_btn = x_coor_btn
    global_y_btn = y_coor_btn

def go():
    '''берём ввод из текстового поля'''
    text_first_num_get = text_first_num.get('1.0', END).strip()

    '''используем глобальные переменные с координатами'''
    x_text = global_x_text
    y_text = global_y_text
    x_btn = global_x_btn
    y_btn = global_y_btn

    '''проверяем, что координаты установлены'''
    if x_text == 0 and y_text == 0:
        print("Ошибка: не установлены координаты текстового поля!")
        return
    if x_btn == 0 and y_btn == 0:
        print("Ошибка: не установлены координаты кнопки!")
        return

    '''теперь наконец-то активируем основную функцию'''
    go_passw(x=x_text, y=y_text,
             x_btn=x_btn, y_btn=y_btn,
             perv_num=text_first_num_get)

tk = Tk()
tk.geometry('800x800')
tk.title('подюор паролей')
'''создаём кнопку для сканирования координат текста куда вводить'''
btn_scan1 = Button(text="Сканировать поле ввода ", command=scan_poz)
btn_scan1.place(x=500, y=200)
'''сканирование координат кнопки для проверки'''
btn_scan_btn = Button(text="Сканировать кнопку", command=scan_poz_btn)
btn_scan_btn.place(x=500, y=500)
'''создаём окно в которое выводятся координаты поля ввода'''
lb_text_coor = Label(text='', width=35, height=5, bg='#919191')
lb_text_coor.place(x=480, y=300)
'''выводим координаты кнопки в окно'''
lb_btn_coor = Label(text='', width=35, height=5, bg='#919191')
lb_btn_coor.place(x=480, y=600)
'''создаём текстовое поле куда пользователь введёт начальные буквы'''
text_first_num = Text(width=27, height=3)
text_first_num.place(x=100, y=300)
'''создаём обозначение для чего это'''
lb_oboz = Label(text='Введите числа которые знаете (первые)', width=40, height=3)
lb_oboz.place(x=40, y=230)
'''создаём кнопку для начинания процесса'''
btn_go = Button(text='go', command=go)
btn_go.place(x=100, y=600)
tk.bind_all('<Control-s>', stop_hotkey)

tk.mainloop()
