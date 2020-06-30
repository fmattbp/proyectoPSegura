from django.template import Template, Context
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from bd import models
import prograSegura.back_end as back_end
from prograSegura.decoradores import *
import os
import base64
import requests
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from datetime import datetime


def login(request):
	t = 'login_v2.html' 
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
				request.session['logueado'] = True
				request.session['usuario'] = usuario
				#respuesta = redirect('/verificar_usuario')
				return redirect('/verificar_usuario')
				#return HttpResponseRedirect(reverse_lazy('verificar_usuario'))
			else:
				return render(request, t,{'errores': 'Usuario o contraseña incorrectos'})
		else:
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
	#token_b64=back_end.generar_token()
	#request.session['token']=token_b64
	if request.method == 'GET' and not request.session.get('verificado', False) :
		print("HOLA")
		if  request.session.get('token_enviado', False):
			return render(request,t,{'errores': 'Token enviado'})
		request.session['token']=back_end.generar_token()
		request.session['timestamp']=datetime.timestamp(datetime.now())
		print("HOLA2")
		#test = back_end.telegram_bot_sendtext(token_b64)
		#prueba=request.session.get('token')
		#token=request.session.get('token')

		back_end.telegram_bot_sendtext(request.session.get('token'))
		request.session['token_enviado'] = True
		return render(request,t)
	elif request.method == 'GET' and request.session.get('verificado', True):
		return redirect('/monitor')

	elif request.method == 'POST':
		#if request.session.get('verificado', True):
			#return redirect('/monitor')
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
					return redirect('/logout')
		else:
			return redirect('/logout')
	#else:
	#	return redirect('/monitor')

@esta_logueado
def monitor(request):
	t='lista.html'
	if request.method == 'GET' and request.session.get('verificado', False):
		return render(request,t)
	else: #request.method == 'GET':
		return redirect('/verificar_usuario')


@esta_logueado
def logout(request):
	request.session.flush()
	respuesta = redirect('/login')
	return respuesta
