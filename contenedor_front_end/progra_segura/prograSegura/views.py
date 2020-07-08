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


def login(request):
	t = 'login.html' 
	if request.method == 'GET' and not request.session.get('logueado', False):
		return render(request, t)
	elif request.method == 'POST' and not request.session.get('logueado', False):
		if back_end.dejar_pasar_peticion_login(request):
			iv_pwd = back_end.convertir_dato_base64(os.urandom(16))
			request.session['iv_pwd'] = iv_pwd
			usuario = request.POST.get('usuario','')
			contra = request.POST.get('password','')
			user2 = authenticate(username=usuario,password=contra)
			if user2 is not None:
				request.session['usuario'] = usuario
				back_end.guardar_contraseña(contra,user2.id,request.session.get('iv_pwd'))
				if request.user.is_active == True:
					return render(request,t,{'errores': 'Este usuario ya tiene una sesión activa'})
				request.session['logueado'] = True
				request.session['id_usuario'] = user2.id
				return redirect('/verificar_usuario')
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
					return redirect('/logout')
		else:
			return redirect('/logout')

@esta_logueado
def monitor(request):
	url_servicios= models.client_server.objects.all().values_list('url_servicios',flat=True).filter(usuario=request.session.get('id_usuario'))
	iv_pwd=request.session.get('iv_pwd')
	usuario = request.session.get('usuario')
	query_contra = models.registrar_contraseña.objects.all().values_list('contraseña',flat=True).filter(usuario=request.session.get('id_usuario'))
	contra_cif = query_contra[0]
	contra = back_end.descifrar(contra_cif,iv_pwd)
	try:
		token = back_end.regresar_token_sesion(url_servicios[0],usuario,contra.decode('utf-8'))
	except:
		return render(request,t{'errores':"Algo fallo al obtener el token")
	if request.method == 'GET' and request.session.get('verificado', False):
		t='lista.html'
		headers = {'Authorization':'Token %s' %token}
		respuesta = requests.get(url_servicios[0]+'/monitor/',headers=headers)
		#for ip in lista_ip_asociada:
		#	print (ip)
			#requests.get("https://",ip,":8000/monitor/")
		#if respuesta.status_code != 200:
		#	return render(request,t,{'errores' : "Forbidden 403"})
		info = respuesta.text
		info = json.loads(info)
		cpu = info['cpu']
		memoria = info['memoria']
		disco = info['disco']
		return render(request,t,{'cpu': cpu,'memoria':memoria,'disco':disco})
		#return render(request,t,{'errores':token})
	else: #request.method == 'GET':
		return redirect('/verificar_usuario')


@esta_logueado
def logout(request):
	request.session.flush()
	respuesta = redirect('/login')
	return respuesta
