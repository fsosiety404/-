'''импортируем библиотеки'''
import os
import hashlib
from cryptography.fernet import Fernet


'''пишем функции для соли ширования подключения к базе данных с pool соеденениями'''

'''создаём функцию для создания рандомной соли'''
def random_salt():
    '''генериуем и возвращаем соль'''
    return os.urandom(16).hex()

'''пишем функцию для шифрования пароля'''
def hash_passw(salt_psw, password):
    '''ппревращаем в байты'''
    salt_enc = salt_psw.encode()
    pasw_enc = password.encode()

    '''хэшируем'''
    hash_pasw = hashlib.pbkdf2_hmac('sha256', pasw_enc, salt_enc, 10000)

    '''возвращаем значение'''
    return hash_pasw.hex()

'''теперь пишем функцию для шифрования с помощью ключа шифрования функцию для шифрования email'''
def shif_fernet(text, key):
    '''превращаем ключ в байты'''
    key_enc = key.encode()
    '''далее создаём обьект клб=юча для шифрования'''
    key_shif = Fernet(key_enc)

    '''алее шифруем'''
    shif_email = key_shif.encrypt(text.encode())

    '''возвращаем значение'''
    return shif_email.decode()

'''пишем функцию для расшифровки'''
def decrypt_fernet(text, key):
    '''преобразум в байты вводы'''
    text_enc = text.encode()
    key_enc = key.encode()

    '''создаём ключ тоесть обьект с помощью шифрования'''
    _key_ = Fernet(key_enc)

    dec_key = _key_.decrypt(text_enc)

    '''возвращаем ключ'''
    return dec_key.decode()
