from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Users
from django.views.decorators.http import require_http_methods
from .utils import hash_passw, shif_fernet, random_salt
from dotenv import load_dotenv
import os
from .utils import *
from datetime import date
import random

'''загружаем env'''
load_dotenv()

'''создаём страничку регестрации ну просто отображаем'''
def main_reg(request):
    if request.session.get('logget'):
        return redirect('main_menu')

    return render(request, 'file_hhtml_test.html')

def serv_reg(request):
    '''для начала определяем метод'''
    if request.method == 'POST':
        '''берём значениее с форм'''
        us_name = request.POST.get('username')
        pasw_user = request.POST.get('password')
        email_user = request.POST.get('email')
        '''создаём сессии'''
        request.session['user_nm'] = us_name
        try:
            '''хэшируем пароль и email'''
            rn_salt = random_salt()

            hash_pasw = hash_passw(salt_psw=rn_salt, password=pasw_user)
            email_fernet = shif_fernet(key=os.getenv('SHIF_KEY'), text=email_user)

            '''сохраняем пользователя'''
            user_reg = Users.objects.create(user_name=us_name, password=hash_pasw, email_user = email_fernet, salt_password = rn_salt)
            '''логиним пользователя оесть сохраняем сессии'''
            request.session['logget'] = True


            return redirect('main_menu')
        except Exception:
            return HttpResponse(f'произошли не поладки со стороны сервера извеняемся за неудобство', status=500)

'''делаем страничку логина'''
def login_client(request):
    return render(request ,'login.html')

'''делаем заднюю сторону логина'''
def login_serv(request):
    try:
        if request.session.get('logget'):
            return redirect('main_menu')
        '''берём значения с формы'''
        user_name_login = request.POST.get('name_login')
        password_login = request.POST.get('password_login')
        '''получаемм пользователя с его ник нейма'''
        user_login_get = Users.objects.get(user_name=user_name_login)

        '''распределяем ответ в переменные'''
        password_hash_login = user_login_get.password
        salt_db_login = user_login_get.salt_password
        '''хэшируем пароль которы ввёл пользователь солью которая с базы данных'''
        hash_login_password_us = hash_passw(salt_psw=salt_db_login, password=password_login)
        '''и теперь сравниваем'''
        if hash_login_password_us == password_hash_login:
            '''сохраняем сессии'''
            request.session['user_nm'] = user_login_get.user_name
            request.session['logget']=True
            return redirect('main_menu')
        else:
            return HttpResponse('неправилно введён пароль или имя', status=500)
    except Exception:
        return HttpResponse('неправильно введён пароль или имя', status=500)


'''делаем страничку которая осле успешной регистрации прововдит на другу страничку'''
def main_menu(request):
    '''берём сессии'''
    user_name = request.session.get('user_nm')
    if not request.session.get('logget', False):
        return redirect('home')

    return render(request, 'main_menu.html', {'username': user_name})

'''делаем страниичку проверки пароля ради того что бы при в ходе в настройки запросить пароль'''
def verf_password_settings(request):


    return render(request, 'verefi_password_to_settings.html')

'''делаем серверную часть'''
def serv_verf_password(request):
    '''получаем данные с формы'''
    password_get = request.POST.get('password')
    '''ищем в базе данных соль и пароль хэшируемый'''
    '''берём данные из сессии '''
    user_name_s_get = request.session.get('user_nm')
    '''обращаемся к базе данных что бы получаить данные'''
    request_to_db = Users.objects.get(user_name=user_name_s_get)
    '''аспределяем ответ базы данных'''
    password_db_hash = request_to_db.password
    salt_db_password = request_to_db.salt_password
    '''хэшируем пароль ввода'''
    password_hash_client = hash_passw(salt_psw=salt_db_password, password=password_get)
    '''теперь сравниваем'''
    if password_hash_client != password_db_hash:
        return HttpResponse('еправильно введён пароль', status=500)
    else:
        return redirect('settings_user')

'''делаем функцию настроек'''
def settings(request):
    if not request.session.get('logget'):
        return redirect('home')

    '''абираем сессию имени'''
    user_name_session = request.session.get('user_nm')

    '''берём данные тоесть нам нужен email'''
    email_get = Users.objects.get(user_name = user_name_session)
    '''достаём зашифрованныё email0'''
    email_enc = email_get.email_user
    '''расшифровываем пароль по ключу шифрования'''
    email_dec = decrypt_fernet(text=email_enc, key=os.getenv('SHIF_KEY'))
    bio = email_get.bio_user
    '''определяем сегодняшний день'''
    time_reg = date.today()

    '''теперь отображаем в html '''

    return render(request, 'settings.html', {'email': email_dec, 'username':user_name_session, 'bio': bio, 'last_password_change':time_reg})

'''делаем страничку на которой сохраняем обновления профиля'''
def upd_profil_(request):
    '''берём ввод поьзователя'''
    vvod_email = request.POST.get('email')
    vvod_bio = request.POST.get('bio')
    '''шифруем ввод что бы добавить в базу данных'''
    email_sh = shif_fernet(text=vvod_email, key=os.getenv('SHIF_KEY'))
    '''теперь берём данные с  сессии тоесть ниик нейм'''
    sesion_user_name = request.session.get('user_nm')
    '''теперь обновляем данные в базе'''
    us_db_get = Users.objects.get(user_name = sesion_user_name)
    us_db_get.email_user = email_sh
    us_db_get.bio_user = vvod_bio

    us_db_get.save()

    '''перенаправляем на главную'''
    return redirect('main_menu')

'''создаём функцию для удаления аккаунта'''
def del_user(request):
    return redirect('logout_user')

'''делаем функцию для смены пароля'''
def ch_password(request):
    req_passwod = request.POST.get('current_password')
    new_password_vvod = request.POST.get('new_password')
    conf_passw = request.POST.get('confirm_password')
    '''берём данные сессии'''
    session_name = request.session.get('user_nm')
    '''теперь ищем пароль с базы данного пользователя'''
    user_get_pasw = Users.objects.get(user_name=session_name)
    '''теперь распределяем в переменную пароль с базы'''
    passwoord_db = user_get_pasw.password
    salt_db = user_get_pasw.salt_password
    '''теперь хэшируем провеерочное поле ввода пароля для сравнения'''
    con_passw_hash = hash_passw(salt_psw=salt_db, password=req_passwod)
    '''и теперь сравниваем'''
    if con_passw_hash != passwoord_db:
        return HttpResponse('неправильно введён текущий пароль', status=500)
    '''а теперь еслии правильно'''
    if con_passw_hash == passwoord_db:
        '''создаём новую соль'''
        new_salt = random_salt()

        '''перь хэшируем новый пароль'''
        new_pasw_hash = hash_passw(salt_psw=new_salt, password=new_password_vvod)
        ''' тперь подверждающий пароь'''
        conf_pasw_hhash = hash_passw(password=conf_passw, salt_psw=new_salt)
        '''и опять сравниваем'''
        if conf_pasw_hhash != new_pasw_hash:
            return HttpResponse('неправильно введён подверждающий пароль', status=500)
        '''а теперь если правильно'''
        if conf_pasw_hhash == new_pasw_hash:
            '''еперь обновляем данные в базе данных'''
            user_get_pasw.password = new_pasw_hash
            user_get_pasw.salt_password = new_salt

            user_get_pasw.save()
            '''и перенаправляем на основную страничку'''
            return redirect('main_menu')

'''делаем логирование но так как нам pythonanywhere не позволяет много места что бы хранить данные
то мы просто отдадим их в другой скрипт ввиде djson  сохраним в отдельный файл'''
@require_http_methods(['GET'])
def api_users_req(request):
    '''создаём предварительные данные для отправки ноо для начала берём данные с базы данных'''
    get_db_users = Users.objects.all()
    '''берём количество'''
    get_count_users_db = Users.objects.count()

    users_ls = []

    for users in get_db_users:
        users_ls.append({
            'id': users.id,
            'us_name': users.user_name,
            'cr_dat': users.created_dat,
            'bio': users.bio
        })
    '''теперь готовим данные для отправки'''
    send_dat = {
        'users_all': users_ls,
        'result': 'good',
        'count_users': get_count_users_db
    }
    '''возвращаем значение'''
    return JsonResponse(send_dat)

'''создаём функцию для отсылания рандомного юзера из бд'''
@require_http_methods(['GET'])
def api_get_rn_user(request):
    get_all_users = Users.objects.all()
    '''теперь мы  распределяем в список наших изеров из бд'''
    users_all = []

    for all_us in get_all_users:
        users_all.append({
            'id': all_us.id,
            'user_nm': all_us.user_name,
            'created_date': all_us.created_dat,
            'bio_user': all_us.bio
        })

    '''теперь на рандом берём рандомного юзера'''

    random_us = random.choice(users_all)

    '''формируем ответ от сервера'''
    send_info_serv = {
        'send_result': 'good',
        'user': random_us
    }

    '''отправляем наш ответ '''
    return JsonResponse(send_info_serv)

'''делаемм страниичку для выхода которая обработает выход и удалит все сессии'''
def logout(request):
    '''просто удаляем'''
    request.session.clear()
    '''перенаправляем на следующую страничку'''
    return redirect('home')
