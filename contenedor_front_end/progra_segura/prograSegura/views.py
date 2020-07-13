from django.template import Template, Context
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from bd import models
import prograSegura.back_end as back_end
from prograSegura.decoradores import *
import os
import requests
from datetime import datetime
import json
from prograSegura import excepciones
import logging
logger = logging.getLogger("django")

def login(request):
	t = 'login.html' 
	if request.method == 'GET' and not request.session.get('logueado', False):
		return render(request, t)
	elif request.method == 'POST' and not request.session.get('logueado', False):
		if back_end.dejar_pasar_peticion_login(request):
			usuario = request.POST.get('usuario','')
			contra = request.POST.get('password','')
			user2 = authenticate(username=usuario,password=contra)
			if user2 is not None:
				if request.user.is_active == True:
					return render(request,t,{'errores': 'Este usuario ya tiene una sesión activa'})
				logger.info("[INFO] ACCESS: %s" % usuario)
				request.session['logueado'] = True
				request.session['id_usuario'] = user2.id
				return redirect('/verificar_usuario')
			else:
				logger.warning("[WARNING] INVALID_CREDENTIALS: %s " % usuario)
				return render(request, t,{'errores': 'Usuario o contraseña incorrectos'})
		else:
			logger.warning("[WARNING] EXCEEDED_TRY_ATTEMPS %s" % usuario)
			return render(request,t,{'errores': 'Demasiados intentos fallidos'})
	elif request.method == 'GET' and request.session.get('logueado', False):
		return redirect('/monitor')
	elif request.method == 'POST' and request.session.get('logueado', False):
		return redirect('/monitor')

@esta_logueado
def generar_nuevo_token(request):
	request.session['token_enviado'] = False
	return redirect('/verificar_usuario')

@esta_logueado
def verificar_usuario(request):
	t = 'verificar_usuario.html'
	if request.method == 'GET' and not request.session.get('verificado', False) :
		if  request.session.get('token_enviado', False):
			return render(request,t,{'errores': 'Token enviado'})
		request.session['token']=back_end.generar_token()
		request.session['timestamp']=datetime.timestamp(datetime.now())
		back_end.telegram_bot_sendtext(request.session.get('token'))
		request.session['token_enviado'] = True
		return render(request,t)
	elif request.method == 'GET' and request.session.get('verificado', True):
		return redirect('/monitor')
	elif request.method == 'POST':
		delta=datetime.now() - datetime.fromtimestamp(request.session.get('timestamp'))
		if delta.total_seconds()< 120:
			codigo_usr = request.POST.get('codigo','')
			if codigo_usr == request.session.get('token'):
				del request.session['token']
				request.session['verificado'] = True
				return redirect('/monitor')
			else:
				if request.session.get('verificado', False):
					return redirect('/monitor')
				else:
					logger.warning("[WARNING] INVALID_TOKEN")
					return redirect('/logout')
		else:
			logger.warning("[WARNING] EXPIRED_TOKEN")
			return redirect('/logout')

@esta_logueado
def tabla(request):
	id_usuario = request.session.get('id_usuario')
	if request.method == 'GET' and request.session.get('verificado', False):
		t='tabla.html'
		try:
			lista_diccionario = back_end.recuperar_token_url(id_usuario)
		except excepciones.TokenException as err:
			return render(request,t,{'errores': err})
		lista_datos_monitoreo = back_end.regresar_datos_monitoreo(lista_diccionario)
		return render(request,t,{'lista_datos': lista_datos_monitoreo})
	else: #request.method == 'GET':
		return redirect('/verificar_usuario')
@esta_logueado
def monitor(request):
	if request.method == 'GET' and request.session.get('verificado', False):
		t='prueba.html'
		return render(request,t)
	else:
		return redirect('/verificar_usuario')


@esta_logueado
def logout(request):
	request.session.flush()
	respuesta = redirect('/login')
	return respuesta
