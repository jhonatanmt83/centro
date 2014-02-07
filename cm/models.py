# -*- encoding: utf-8 -*-
from django.db import models

# Create your models here.


class Paciente(models.Model):
    class Meta:
        verbose_name = ('Paciente')
        verbose_name_plural = ('Pacientes')

    nombres = models.CharField(max_length=200, verbose_name=u'Nombres y Apellidos')
    direccion = models.CharField(max_length=200, verbose_name=u'Dirección')
    edad = models.IntegerField(verbose_name=u'Edad')
    fechanacimiento = models.DateField(verbose_name=u'Fecha de Nacimiento')
    telefono = models.CharField(max_length=9, verbose_name=u'Teléfono')
    nrohistoria = models.CharField(max_length=6, verbose_name=u'N° de Historia Clínica')
    edadfur = models.DateField(verbose_name=u'Edad FUR', null=True, blank=True)
    null_edadfur = models.BooleanField(verbose_name=u'No recuerda')
    ultimofur = models.DateField(verbose_name=u'FUR', null=True, blank=True)
    null_ultimofur = models.BooleanField(verbose_name=u'No recuerda')
    fecha = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.nombres


class Antecedente(models.Model):
    class Meta:
        verbose_name = ('Antecedente')
        verbose_name_plural = ('Antecedentes')

    personales = models.TextField(verbose_name=u'Personales')
    familiares = models.TextField(verbose_name=u'Familiares')
    cancer = models.TextField(verbose_name=u'Cancer')
    otros = models.TextField(verbose_name=u'Otros')

    def __unicode__(self):
        pass
    