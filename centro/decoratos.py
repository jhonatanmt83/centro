#-*- coding:utf-8 -*-

# from django.contrib.auth.models import User,Group
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def registrador_login(view_func):
    def wrap(request, *args, **kwargs):
        is_doc = request.user.groups.filter(name='Registrador').count()
        if request.user.is_authenticated() and is_doc :
            return view_func( request=request,*args, **kwargs )
        return HttpResponseRedirect(reverse('home'))
    wrap.__doc__ = view_func.__doc__
    wrap.__dict__ = view_func.__dict__
    return wrap


def evaluador_login(view_func):
    def wrap(request, *args, **kwargs):
        is_sec = request.user.groups.filter(name='Evaluador').count()
        if request.user.is_authenticated() and is_sec :
            return view_func( request=request,*args, **kwargs )
        return HttpResponseRedirect(reverse('home'))
    wrap.__doc__ = view_func.__doc__
    wrap.__dict__ = view_func.__dict__
    return wrap




def administrador_login(view_func):
    def wrap(request, *args, **kwargs):
        is_dir = request.user.groups.filter(name='Administrador').count()
        if request.user.is_authenticated() and is_dir :
            return view_func( request=request,*args, **kwargs )
        return HttpResponseRedirect(reverse('home'))
    wrap.__doc__ = view_func.__doc__
    wrap.__dict__ = view_func.__dict__
    return wrap
