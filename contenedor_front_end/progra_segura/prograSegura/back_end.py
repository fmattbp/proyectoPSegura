from bd import models
import datetime
import prograSegura.settings as settings
#from cryptography.hazmat.backends import default_backend
#from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import base64
import requests

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

def convertir_dato_base64(dato):
    return base64.b64encode(dato).decode('utf-8')

def convertir_base64_dato(dato_b64):
    return base64.b64decode(dato_b64)


def telegram_bot_sendtext(bot_message):

    #bot_token = '1201671700:AAGvvO00k_rrVJiokhCJsL1SfmzY6BK578k'
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

