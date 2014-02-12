#-*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.template import RequestContext

from centro.decoratos import registrador_login, evaluador_login, administrador_login
from django.http import HttpResponseRedirect, HttpResponse

from cm.forms import PerfilForm, PacienteForm1, PacienteForm2, PaquetesSeleccionForm, AntecedenteForm
from django.contrib.auth.models import User, Group
from cm.models import Perfil, Paquete

from django.contrib import messages


from django.contrib.auth.forms import UserCreationForm

from datetime import date
import json


# Create your views here.
def home(request):
    if request.user.groups.filter(name='Administrador'):
        return HttpResponseRedirect('/administrador/')
    elif request.user.groups.filter(name='Registrador'):
        return HttpResponseRedirect('/registrador/')
    elif request.user.groups.filter(name='Evaluador'):
        return HttpResponseRedirect('/evaluador/')
    else:
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
        else:
            pass


@registrador_login
def registrador(request):
    return render_to_response('registrador/registrador.html', {}, context_instance=RequestContext(request))


@evaluador_login
def evaluador(request):
    return render_to_response('evaluador/evaluador.html', {}, context_instance=RequestContext(request))


@administrador_login
def administrador(request):
    return render_to_response('administrador/administrador.html', {}, context_instance=RequestContext(request))


@administrador_login
def nuevo_usuario(request):
    if request.method=='POST':
        formulario = UserCreationForm(request.POST)
        formulario_perfil = PerfilForm(request.POST)
        if formulario.is_valid() and formulario_perfil.is_valid():
            nuevo_usuario = User.objects.create_user(request.POST['username'], '', request.POST['password1'])
            nuevo_usuario.save()
            nuevo_perfil = Perfil(usuario=nuevo_usuario, dni=request.POST['dni'], nombres=request.POST['nombres'], profesion=request.POST['profesion'], direccion=request.POST['direccion'], sueldo=request.POST['sueldo'])
            nuevo_perfil.save()
            grupo_seleccionado = Group.objects.get(pk=request.POST['rol'])
            nuevo_usuario.groups.add(grupo_seleccionado)
            messages.success(request, 'Nuevo usuario %s creado'% (request.POST['username']))
            formulario = UserCreationForm
            formulario_perfil = PerfilForm
    else:
        formulario = UserCreationForm
        formulario_perfil = PerfilForm
    return render_to_response('administrador/nuevo_usuario.html', {'formulario': formulario, 'formulario_perfil': formulario_perfil}, context_instance=RequestContext(request))


@administrador_login
def nuevo_paciente(request):
    if request.method=='POST':
        formulario = UserCreationForm(request.POST)
        formulario_perfil = PerfilForm(request.POST)
        if formulario.is_valid() and formulario_perfil.is_valid():
            nuevo_usuario = User.objects.create_user(request.POST['username'], '', request.POST['password1'])
            nuevo_usuario.save()
            nuevo_perfil = Perfil(usuario=nuevo_usuario, dni=request.POST['dni'], nombres=request.POST['nombres'], profesion=request.POST['profesion'], direccion=request.POST['direccion'], sueldo=request.POST['sueldo'])
            nuevo_perfil.save()
            grupo_seleccionado = Group.objects.get(pk=request.POST['rol'])
            nuevo_usuario.groups.add(grupo_seleccionado)
            messages.success(request, 'Nuevo usuario %s creado'% (request.POST['username']))
            formulario = UserCreationForm
            formulario_perfil = PerfilForm
    else:
        formulario1 = PacienteForm1
        formulario2 = PacienteForm2(initial={'fecha_actual': date.today()})
        paquetesform = PaquetesSeleccionForm
        antecedentesform = AntecedenteForm
        paquetes = Paquete.objects.all()
        print (dir(paquetes[0].tiposexamen.values))
        print paquetes[0].tiposexamen.values
    return render_to_response('administrador/nuevo_paciente.html', {'formulario1': formulario1, 'formulario2': formulario2, 'paquetesform': paquetesform, 'antecedentesform': antecedentesform, 'paquetes': paquetes}, context_instance=RequestContext(request))


def precio_paquete(request, codigo):
    """Devuelve el precio correspondiente al paquete"""
    paquete = Paquete.objects.get(pk=int(codigo))
    new_result = []
    datos = {}
    datos['precio'] = str(paquete.precio_total())
    new_result.append(datos)
    return HttpResponse(json.dumps(new_result))
