from bd import models
import datetime
import prograSegura.settings as settings
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import base64
import requests
import json
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def dejar_pasar_peticion_login(request):
    ip = get_client_ip(request)
    timestamp = datetime.datetime.now(datetime.timezone.utc)
    try:
        registro = models.IPs.objects.get(ip=ip)
    except: # la ip nunca ha hecho peticiones
        nuevoRegistroIP = models.IPs(ip=ip, ultima_peticion=timestamp, intentos=1)
        nuevoRegistroIP.save()
        return True
    diferencia = (timestamp - registro.ultima_peticion).seconds
    if diferencia > settings.VENTANA_TIEMPO_INTENTOS_LOGIN:
        registro.ultima_peticion = timestamp
        registro.intentos=1
        registro.save()
        return True
    elif settings.INTENTOS_LOGIN > registro.intentos:
        registro.ultima_peticion = timestamp
        registro.intentos = registro.intentos+1
        registro.save()
        return True
    else:
        registro.ultima_peticion = timestamp
        registro.intentos = registro.intentos+1
        registro.save()
        return False

def guardar_contraseña(contra,id,iv):
    try:
        registro = models.registrar_contraseña.objects(usuario=id)
    except:
        contra_cif = cifrar(contra,convertir_base64_dato(settings.LLAVE_AES.encode('utf-8')),convertir_base64_dato(iv.encode('utf-8')))
        nuevo_registro = models.registrar_contraseña(usuario=id,contraseña=contra_cif)
        nuevo_registro.save()
        return True
    models.registrar_contraseña.objects.filter(usuario=id).delete()
    contra_cif = cifrar(contra,convertir_base64_dato(settings.LLAVE_AES.encode('utf-8')),convertir_base64_dato(iv.encode('utf-8')))
    nuevo_registro = models.registrar_contraseña(usuario=id,contraseña=contra_cif)
    nuevo_registro.save()
    return True


def convertir_dato_base64(dato):
    return base64.b64encode(dato).decode('utf-8')

def convertir_base64_dato(dato_b64):
    return base64.b64decode(dato_b64)


def telegram_bot_sendtext(bot_message):

    bot_token = '1103526254:AAG_7HV2xPhrN6W-m17sB2KwKV3DUNC7RL0'
    bot_chatID = '-417703328'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

def generar_token():
    codigo = os.urandom(6)
    codigo=convertir_dato_base64(codigo)
    token=''
    for letra in codigo:
        if letra=="I":
            letra="i"
        if letra=="l":
            letra="L"
        if letra=="+":
            letra="x"
        token=token+letra
    return token


def regresar_token_sesion(url_servicios,usuario,contra):
    url_token = url_servicios + '/autenticacion/'
    data = {'username': usuario, 'password': contra}
    respuesta = requests.post(url_token, data=data)
    if respuesta.status_code != 200:
        raise excepciones.TokenException('No se pudo recuperar el token: %s' % respuesta.status_code)
    else:
        diccionario = json.loads(respuesta.text)
        return diccionario['token']


def cifrar(mensaje,llave_aes, iv):
    aesCipher = Cipher(algorithms.AES(llave_aes), modes.CTR(iv),
                       backend=default_backend())
    cifrador = aesCipher.encryptor() 
    cifrado = cifrador.update(mensaje.encode('utf-8'))
    cifrador.finalize()
    return convertir_dato_base64(cifrado)

def descifrar(cifrado, iv):
    llave_aes = convertir_base64_dato(settings.LLAVE_AES.encode('utf-8'))
    iv = convertir_base64_dato(iv.encode('utf-8'))
    cifrado = convertir_base64_dato(cifrado)
    aesCipher = Cipher(algorithms.AES(llave_aes), modes.CTR(iv),
                       backend=default_backend())
    descifrador = aesCipher.decryptor()
    plano = descifrador.update(cifrado)
    descifrador.finalize()
    return plano
