import requests
import os

'''определяем имя пользователя'''
us_nm_user = os.getlogin()

try:
    '''читаем текст из файла'''
    with open(f'/home/{us_nm_user}/file_python_cs.txt', 'r', encoding='utf-8') as file:
        text_from_file = file.read()


except FileNotFoundError:
    print(f"Ошибка: Файл /home/{us_nm_user}/file_python_cs.txt не найден")

'''отправляем запрос где отдаём данные а сервер отдаёт результат'''
select = input("Введите URL и endpoint сайта: ")

'''запрашиваем пароль'''
password = input("введите пароль для отправки (его запросит сервер):   ")

'''составляем json'''
req_json = {
    'text': text_from_file,
    'password': password
}

try:
    '''отправляем запрос'''
    print(f"send request for {select}...")
    request_post_to_server = requests.post(url=select, json=req_json, timeout=10)

    '''проверяем статус ответа'''
    if request_post_to_server.status_code == 200:
        '''получаем JSON ответ'''
        otv_server = request_post_to_server.json()

        '''проверяем значение которое возвращает сервер'''
        if otv_server.get('result-req') == 'success! admin panel created by fsociety404 github: https://github.com/fsosiety404/-':
            print("success! reload server to apply changes")
        else:
            print(f'error request {otv_server.get('result-req')}')

except requests.exceptions.ConnectionError:
    print(f"Ошибка подключения")
