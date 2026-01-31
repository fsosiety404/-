from dotenv import load_dotenv
from cryptography.fernet import Fernet
import os
import hashlib
import psycopg2
from psycopg2 import pool
from psycopg2.pool import SimpleConnectionPool

'''загружаем .env файл'''
load_dotenv()

'''создаём функцию для шифрования'''
def encrypt_fernet(email_or_other, shif_key):
    arg_key = shif_key.encode()
    _key_ = Fernet(arg_key)
    shifrov = _key_.encrypt(email_or_other.encode())
    return shifrov.decode()


'''создаём функцию для расшифрования'''
def decrypt_fernet(text, key):
    dec_key = key.encode()
    sh_key = Fernet(dec_key)
    otv_decrypt = sh_key.decrypt(text.encode())
    return otv_decrypt.decode()


'''функция для подключения базы данных'''
def connect_to_db():
    '''подключаемся к базе данных и загружаем информацию в файле .env'''
    conn = psycopg2.pool.ThreadedConnectionPool(
        minconn=1,
        maxconn=25,
        port=os.getenv('PORT_DB'),
        host=os.getenv('HOST_DB'),
        user=os.getenv('USER_BD'),
        password=os.getenv('BD_PASSWORD'),
        database=os.getenv('DATABASE')
        )
    return conn



'''создаём функцию которая создаёт случайную salt с помощью которой даже одинаковые пароли будут разными в базе данных'''


def random_salt():
    '''генерируем salt и возвращаем значение'''
    return os.urandom(16).hex()


'''создаём функцию которая принимает в аргументы пароль и salt и после их складывает и хэширует по алгоритму sha256'''


def hash_pasw_pbkdf2(password, salt):
    password_func = password.encode()
    salt_func = salt.encode()
    has_pbkdf2 = hashlib.pbkdf2_hmac('sha256', password_func, salt_func, 10000)

    return has_pbkdf2.hex()
