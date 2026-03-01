**это  админ панель desktop версия через неё можно управлять текстом сайта его и тд**
**что бы этот код работал и менял текст в вашем сайте для начала вам нужно добавить в ваш проект Django (пока только django так как пока на нём знаю как принимать и отдавать api)**
**и так что бы текст в сайте работал корректно нужно в сайт  с определённым endpoint в ваш сайт нужно добавить код который всё это обработает**
**вот код:**
````
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

password_adm = "very-secret-key123" # тут можно ввести ваш пароль просто поменяйте значение
text_admn = "" # тут надо по желанию поставить дефолтное значение которое отобразится

@csrf_exempt
@require_http_methods(['POST'])
def http_text_ren_serv(request):
    global text_admn
    '''получаем данные запроса'''
    data = json.loads(request.body)

    '''сверяем пароль'''
    if data['password'] == password_adm:
        '''обрабатываем'''
        _text_adm_ = data['text']
        '''передаём в глобальную переменную'''
        text_admn = _text_adm_

        '''возвращаем json ответ'''
        return JsonResponse({
        'result-req': 'success! admin panel created by fsociety404 github: https://github.com/fsosiety404/-'
        })
    else:
        return JsonResponse({
            'result-req': 'неправильно введён пароль! admin panel created by fsociety404 github: https://github.com/fsosiety404/-'
        })


def main_st(request):
    return render(request, 'chat.html', {'text': text_admn}) # это пример вам для отображения нового текста надо вписать переменную на другую страничку
````

**и ОБЯЗАТЕЛЬНЫЙ ШАГ в код с url обычно эт urls.py добавте эту строчку для отключения csrf защиты django (у меня код отличается так как
я файл urls.py добавил в папку с файлами models.py views.py и тд вам тоже желательно так добавить) вот код:**

````
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', views.main_st, name='home'),
    path('api_adm/', csrf_exempt(views.http_text_ren_serv), name='api_serv')
]
````
**а в другой базовый urls.py нужно доавить в место прошлого кода этот**

````
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls'))
]
````

**ВАЖНО КАК ЗАПУСКАТЬ: для начала в другом редакторе кода например vs code или rider откройте этот файл И ПОМЕСТИТЕ В КОНСОЛЬНЫЙ ПРОЕКТ СОЗДАЯ ЕГО либо откройте в терминале эту папку и СОЗДАТЬ ПРОЕКТ ТУДА ПОМЕСТИТЬ ЭТОТ ФАЙЛ и выполните эту команду dotnet run так же установите перед эти установите sdk .net
важно из папки которую вы скачали файл поместите в эти места в зависимости от ос file_python_cs.txt  если вы на виндовс то в место C:\Users\ваше имя\Desktop если вы на линуксе то в это место 
/home/ваше имя/ так же если вы хотите прочитать текст файла (это в первом вырианте в Program.cs) то значит фаш файл тоже должен лежать в там же месте
после запуска Program.cs запустите файл read_and_post_file_cs.py  следуёте настройкам так же установите библиотеку request что бы запустить файл после запуска последнегскрипта просто обновите страничку**