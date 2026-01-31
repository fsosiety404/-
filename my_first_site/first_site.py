'''web окно регистрации с переносом в базу данных и хэшированием'''
'''!!!ВНИИМАНИЯ HTML ПИСАЛА НЕЙРОСЕТЬ ТАК КАК Я HTML НЕ УЧИЛ НО ЗНАЮ БАЗУ КОТОРАЯ НУЖНА ДЛЯ FLASK!!!'''

'''ипортируем нужные библиотеки'''
from flask import Flask, session, request, redirect, render_template
from psycopg2 import sql
import psycopg2
import os
from datetime import datetime
from lib_hash_and_fernet_shif import *
from dotenv import load_dotenv

'''создаём переменную которая принимает функцию подключения'''
pool_conn = connect_to_db()

'''создаём атрибут класса name'''
app = Flask(__name__, template_folder='/home/fsosiety/html_files')

'''загружаем .env файл'''
load_dotenv()

'''делаем ключ для сессий тоесть загружаем из .env'''
app.secret_key = os.getenv('SESION_KEY')

'''создаём корневую страничку и берё метод GET'''
@app.route('/', methods=['GET'])
def reg_client():
    '''если челвек уже зарегестрированн по суссии то тогда перерасыаем основную страницу'''
    if session.get('logget'):
        return redirect('/main')
    '''возвращаем html страницу'''
    return render_template('file_hhtml_test.html')


'''создаём страничку которая будет отвечать за главный процесс регистрации'''
@app.route('/register', methods=['POST'])
def serv_reg():
    try:

        '''получаем свободное соеденение'''
        conn = pool_conn.getconn()
        '''создаём переменную которая сможет исполнить наш запрос sql'''
        cur = conn.cursor()

        '''берём ввод пользователя имени пароля email'''
        get_user_name = request.form['username']
        get_email_html = request.form['email']
        get_password_html = request.form['password']

        '''генерируем salt для пароля'''
        salt_password_reg = random_salt()

        '''теперь шифруем пароль с salt'''
        hash_password_html = hash_pasw_pbkdf2(salt=salt_password_reg, password=get_password_html)
        '''а теперь шифруем email с отдельным ключом шифрованием'''
        email_shif = encrypt_fernet(email_or_other=get_email_html, shif_key=os.getenv('SHIF_KEY'))


        '''теперь пишем sql запрос для добавление пароля и salt'''
        sql_insert = sql.SQL('''
        INSERT INTO register_python_hash (user_name, password_user, email, sl_password)
        VALUES (%s, %s, %s, %s)
        ''')

        '''исполняем наш запрос  нужными нам значениями'''
        cur.execute(sql_insert, (get_user_name, hash_password_html, email_shif, salt_password_reg))
        '''сохраняем'''
        conn.commit()

        '''сохраняем сессии что бы несколько раз не пришлось регистрироваться для начала ищем добавленного юзера и выбираем id'''
        sql_select_reg = sql.SQL('''
        SELECT * FROM register_python_hash
        WHERE user_name = %s
        ''')
        '''сполняем наш запрос'''
        cur.execute(sql_select_reg, (get_user_name,))
        '''получем ответ'''
        otv_serv_reg = cur.fetchone()

        '''распределяем ответ в отдельные переменные'''
        session['id_user_session'] = otv_serv_reg[0]
        session['user_name_session'] = get_user_name
        session['logget'] = True

        '''делаем сессию постоянной'''
        session.permanent = True

        '''передаём соседенение другому поьзователю что бы сервер не лёг от переизбытка запросов (желательно добавить ассинхронность но я этому ещё не научился)'''
        cur.close()
        pool_conn.putconn(conn)

        '''перекидываем на страничку если успешно и не произошли неполадки'''
        return redirect('/main')
    except Exception:
        return f'<h1>произошли неполадки со стороны сервера извеняемся за неудобство<h1>', 500


'''делаем страничку для входа просто изобразим'''
@app.route('/login-in-acaunt', methods=['GET'])
def login_client():
    return render_template('login.html')


'''теперь делаем серверную часть login'''
@app.route('/login', methods=['POST'])
def login_in_acaunt():
    try:
        conn = pool_conn.getconn()
        cur = conn.cursor()
        '''берём ввода'''
        us_name_get = request.form['name_login']
        passw_get = request.form['password_login']
        '''пишем sql запрос поиска email'''
        sql_select_login = sql.SQL('''
        SELECT * FROM register_python_hash
        WHERE user_name = %s
        ''')
        '''исполняем наш запрос'''
        cur.execute(sql_select_login, (us_name_get,))
        '''получаем ответ'''
        otv_serv = cur.fetchone()
        '''если не найдет сообщаем'''
        if not otv_serv:
            return '<h1>пользователь не найден<h1>'

        pasw_hash_otv_serv = otv_serv[2]
        salt_pasw_otv_serv = otv_serv[4]
        user_id = otv_serv[0]
        '''тепеь хэшируем ввод пользователя по такой же соли и после сравнимаем'''
        hash_htmll_pasw = hash_pasw_pbkdf2(salt=salt_pasw_otv_serv, password=passw_get)

        if hash_htmll_pasw != pasw_hash_otv_serv:
            return '<h1>неправильно введён пароль<h1>'
        if hash_htmll_pasw == pasw_hash_otv_serv:
            '''сщздаём сессии'''
            session['id_user_session'] = user_id
            session['user_name_session'] = us_name_get
            session['logget'] = True
            session.permanent = True
            cur.close()
            pool_conn.putconn(conn)
            return redirect('/main')
    except Exception:
        return f'<h1>произошла ошибка со стороны сервера извеняемся за неудобство<h1>', 500


'''делаем другую страничку для  того что бы мы знали страничку'''
@app.route('/main', methods=['GET'])
def main_menu():
    '''берём сессии'''
    session_us_name = session.get('user_name_session')

    '''делаеем что бы пользователь не  зарегестрировшийся не мог просто взять и по ссылки перейти'''
    if not session.get('logget'):
        return redirect('/')

    conn = pool_conn.getconn()
    cur = conn.cursor()
    '''пишем sql запрос что бы получить id что бы после отобразить его'''
    sql_select_main = sql.SQL('''
    SELECT id_user, user_name FROM register_python_hash
    WHERE user_name = %s
    ''')
    cur.execute(sql_select_main, (session_us_name,))
    '''получаем ответ'''
    otv_id_serv_main = cur.fetchone()
    '''теперь распределим ответ в переменную'''
    id_user_main = otv_id_serv_main[0]
    us_name = otv_id_serv_main[1]

    '''определяем дату и всё остальное'''
    otv = datetime.now()
    '''теперь берём от тутого только  дату тоесть год месяц и день'''
    dat = otv.strftime('%d.%m.%Y')

    cur.close()
    pool_conn.putconn(conn)

    '''возвращаем страницу html с данными'''
    return render_template('main_menu.html', username=us_name, user_id=id_user_main, reg_date=dat)


'''делаем страничку для настройек пользователя'''
@app.route('/settings', methods=['GET'])
def settings_client():
    try:
        '''делаем страничку для настройек пользователя'''
        '''Проверяем авторизацию'''
        if not session.get('logget'):
            return redirect('/')

        '''Получаем username из сессии'''
        session_user_name_settings = session.get('user_name_session')
        '''получаем ввод bio'''
        bio_user = request.args.get('bio')
        '''созранняем сессию'''
        session['bio_user_session'] = bio_user

        conn = pool_conn.getconn()
        cur = conn.cursor()

        '''Получаем email из БД'''
        sql_select_email = sql.SQL('''
        SELECT email FROM register_python_hash
        WHERE user_name = %s
        ''')

        cur.execute(sql_select_email, (session_user_name_settings,))
        otv_settings_db = cur.fetchone()

        if otv_settings_db:
            email_shif = otv_settings_db[0]
            ''' Расшифровываем email'''
            key_shif_set = os.getenv('SHIF_KEY')
            email_user = decrypt_fernet(text=email_shif, key=key_shif_set)
        else:
            email_user = ""

        '''пишем sql запрос'''
        sql_select_bio = sql.SQL('''SELECT bio FROM register_python_hash WHERE user_name = %s''')

        ''' Получаем bio если есть'''
        cur.execute(sql_select_bio, (session_user_name_settings,))
        bio_result = cur.fetchone()
        bio_user = bio_result[0] if bio_result else ""

        cur.close()
        pool_conn.putconn(conn)

        '''Отображаем страницу с данными'''
        return render_template('settings.html',username=session_user_name_settings,email=email_user,bio=bio_user)
    except Exception:
        return '<h1>произошла ошибка со стороны сервера извеняемся за неудобство<h1>', 500


'''делаем страничку для обновлениия странички основной там мы прогоним всё через функционал обновления'''
@app.route('/update_profile', methods=['POST'])
def update_prfil():
    try:
        '''если нет сессии которая выдаётся после регистрации не даём войти перекидваем к рагистрации'''
        if not session.get('logget'):
            return redirect('/')

        conn = pool_conn.getconn()
        cur = conn.cursor()

        '''берём сессии тоесь id который сохранялся'''
        session_id_get = session.get('id_user_session')
        session_user_name = session.get('user_name_session')
        new_bio = request.form.get('bio')

        '''пишем sql запрос для обновлениия данных'''
        sql_update = sql.SQL('''
        UPDATE register_python_hash
        SET bio = %s,
        user_name = %s
        WHERE id_user = %s
        ''')
        '''исполняем запрос'''
        cur.execute(sql_update, (new_bio, session_user_name, session_id_get))
        conn.commit()
        pool_conn.putconn(conn)

        return redirect('/main')
    except Exception:
        return 'произошли не поладки со стороны сервера извеняемся за неудобство',500


'''пиишем страничку для смене пароля ну которая будет обрабатывать смену пароля'''
@app.route('/change_password', methods=['POST'])
def change_passw():
    if not session.get('logget'):
        return redirect('/')

    try:
        conn = pool_conn.getconn()
        cur = conn.cursor()

        '''берём ввод пользователя'''
        passw_vvod = request.form['current_password']
        new_passw = request.form['new_password']
        povtor_passw = request.form['confirm_password']

        '''берём сессию имени'''
        user_name_session = session.get('user_name_session')

        '''пишем sql запрос что бы найти пароль по имени'''
        sql_select_password_cha = sql.SQL('''
        SELECT password_user, sl_password FROM register_python_hash
        WHERE user_name = %s
        ''')
        '''исполняем запрос'''
        cur.execute(sql_select_password_cha, (user_name_session,))
        '''получаем ответ'''
        otv_serv_pasw_hash = cur.fetchone()
        hash_pasw_ch = otv_serv_pasw_hash[0]
        salt_passw = otv_serv_pasw_hash[1]
        '''теперь хэшируем ввод пользователя и сравниваем'''
        vvod_ch_passw_hash = hash_pasw_pbkdf2(password=passw_vvod, salt=salt_passw)
        '''теперь сравниваем ввод и сам пароль'''
        if vvod_ch_passw_hash == hash_pasw_ch and povtor_passw == new_passw:
            '''теперь хэшируем пароль ввода пользователя с новой солью'''
            random_salt_ch_passw = random_salt()
            '''хэшируем уже ввод пользователя'''
            hash_new_pasw = hash_pasw_pbkdf2(salt=random_salt_ch_passw, password=passw_vvod)

            '''пишем sql запрос для обновления данных'''
            sql_update_ch_passw = sql.SQL('''
            UPDATE register_python_hash
            SET password_user = %s,
            sl_password = %s
            WHERE user_name = %s
            ''')
            '''исполняем запрос'''
            cur.execute(sql_update_ch_passw, (hash_new_pasw, random_salt_ch_passw ,user_name_session))
            conn.commit()

            pool_conn.putconn(conn)
            return redirect('/main')
        if vvod_ch_passw_hash != hash_pasw_ch or povtor_passw != new_passw:
            return redirect('/settings')
    except Exception:
        return f'<h1>извеняемся произошли не поладки со стороны сервера<h1>', 500

'''делаем страничку для удаления аккаунта'''
@app.route('/delete_account', methods=['POST'])
def del_accaunt():
    return redirect('/logout')


@app.route('/logout', methods=['GET'])
def logout_func():
    '''очищаем все сессии'''
    session.clear()
    '''перекидываем к регистрации'''
    return redirect('/')

if __name__ == '__main__':
    app.run()

