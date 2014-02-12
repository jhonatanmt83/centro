# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

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

    personales = models.CharField(max_length=200, verbose_name=u'Personales')
    familiares = models.CharField(max_length=200, verbose_name=u'Familiares')
    cancer = models.CharField(max_length=200, verbose_name=u'Cancer')
    otros = models.CharField(max_length=200, verbose_name=u'Otros')
    paciente = models.ForeignKey(Paciente)

    def __unicode__(self):
        return str(self.paciente)


class UltimaCita(models.Model):
    class Meta:
        verbose_name = ('UltimaCita')
        verbose_name_plural = ('UltimasCitas')

    paciente = models.ForeignKey(Paciente)
    proximo = models.DateField(verbose_name=u'Próxima cita')
    anterior = models.DateField(verbose_name=u'Última cita')

    def __unicode__(self):
        return str(self.paciente)


class DiagnosticoExamen(models.Model):
    class Meta:
        verbose_name = ('DiagnosticoExamen')
        verbose_name_plural = ('Diagnosticos de Examen')

    texto = models.CharField(max_length=100, verbose_name=u'Diagnostico')

    def __unicode__(self):
        return self.texto


#Para la parte de receta

class ClaseMedicamento(models.Model):
    class Meta:
        verbose_name = ('ClaseMedicamento')
        verbose_name_plural = ('ClaseMedicamentos')

    nombre = models.CharField(max_length=100, verbose_name=u'Nombre')

    def __unicode__(self):
        return self.nombre

class TipoCantidad(models.Model):
    class Meta:
        verbose_name = ('TipoCantidad')
        verbose_name_plural = ('TipoCantidades')

    nombre = models.CharField(max_length=100, verbose_name=u'Nombre')

    def __unicode__(self):
        return self.nombre

class Frecuencia(models.Model):
    class Meta:
        verbose_name = ('Frecuencia')
        verbose_name_plural = ('Frecuencias')

    nombre = models.CharField(max_length=100, verbose_name=u'Nombre')

    def __unicode__(self):
        return self.nombre

class DiagnosticoReceta(models.Model):
    class Meta:
        verbose_name = ('DiagnosticoReceta')
        verbose_name_plural = ('DiagnosticoRecetas')

    texto = models.CharField(max_length=100, verbose_name=u'Nombre')

    def __unicode__(self):
        return self.texto


class Medicamento(models.Model):
    class Meta:
        verbose_name = ('Medicamento')
        verbose_name_plural = ('Medicamentos')

    nombre = models.CharField(max_length=100, verbose_name=u'Nombre')
    clase = models.ForeignKey(ClaseMedicamento, verbose_name=u'Clase de Medicamento')
    cantidad = models.ForeignKey(TipoCantidad, verbose_name=u'Tipode Cantidad')

    def __unicode__(self):
        return self.nombre


class Receta(models.Model):
    class Meta:
        verbose_name = ('Receta')
        verbose_name_plural = ('Recetas')

    paciente = models.ForeignKey(Paciente, verbose_name=u'Paciente')
    fecha = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return str(self.paciente)


class DiagnosticoReceta(models.Model):
    class Meta:
        verbose_name = ('DiagnosticoReceta')
        verbose_name_plural = ('DiagnosticoRecetas')

    receta = models.ForeignKey(Receta, verbose_name=u'Receta')
    diagnosticos = models.ManyToManyField(DiagnosticoReceta, verbose_name=u'Diagnósticos')

    def __unicode__(self):
        return self.receta


class Tratamiento(models.Model):
    class Meta:
        verbose_name = ('Tratamiento')
        verbose_name_plural = ('Tratamientos')

    tipo_duracion = (
        ('di', 'Dias'),
        ('se', 'Semanas'),
        ('me', 'Meses'),
    )

    medicamento = models.ForeignKey(Medicamento, verbose_name=u'Medicamento')
    cantidad = models.IntegerField(verbose_name=u'Cantidad')
    cantidaddosis = models.IntegerField(verbose_name=u'Cantidad de dosis')
    frecuencia = models.ForeignKey(Frecuencia, verbose_name=u'Frecuencia')
    duracion = models.IntegerField(verbose_name=u'Duración')
    tipoduracion = models.CharField(max_length=2,
                                    choices=tipo_duracion,
                                    default='di')

    def __unicode__(self):
        return self.receta


class Egreso(models.Model):
    class Meta:
        verbose_name = ('Egreso')
        verbose_name_plural = ('Egresos')

    usuario = models.ForeignKey(User, verbose_name=u'Usuario')
    monto = models.DecimalField(max_digits=6, decimal_places=2)
    descripcion = models.TextField(verbose_name=u'Descripción')
    dni = models.CharField(max_length=8, verbose_name=u'DNI')
    fecha = models.DateField(auto_now_add=True)
    pagouotro = models.BooleanField('Tipo de Pago')

    def __unicode__(self):
        return self.usuario


#Para la parte de los exmanes

class TipoExamen(models.Model):
    class Meta:
        verbose_name = ('Tipo de Examen')
        verbose_name_plural = ('Tipos de Examenes')

    nombre = models.CharField(max_length=100, verbose_name=u'Nombre')
    fechacreacion = models.DateField(auto_now_add=True)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre
    

class ItemExamen(models.Model):
    class Meta:
        verbose_name = ('ItemExamen')
        verbose_name_plural = ('ItemsExamenes')

    texto = models.CharField(max_length=100, verbose_name=u'Texto')
    tipoexamen = models.ForeignKey(TipoExamen)

    def __unicode__(self):
        return self.texto


class SubItemExamen(models.Model):
    class Meta:
        verbose_name = ('SubItemExamen')
        verbose_name_plural = ('SubItemsExamenes')

    texto = models.CharField(max_length=100, verbose_name=u'Texto')
    item = models.ForeignKey(ItemExamen)

    def __unicode__(self):
        return self.texto


class Paquete(models.Model):
    class Meta:
        verbose_name = ('Paquete')
        verbose_name_plural = ('Paquetes')

    nombre = models.CharField(max_length=100, verbose_name=u'Nombre')
    activo = models.BooleanField(default=True)
    tiposexamen = models.ManyToManyField(TipoExamen)

    def __unicode__(self):
        return self.nombre

    def precio_total(self):
        pass


class Examen(models.Model):
    class Meta:
        verbose_name = ('Examen')
        verbose_name_plural = ('Examenes')

    paciente = models.ForeignKey(Paciente, related_name='examen_paciente')
    paquetes = models.ManyToManyField(Paquete, related_name='examen_paquetes', null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)
    fecha_editado = models.DateField(auto_now=True)
    recomendaciones = models.TextField()
    terminado = models.BooleanField(default=False)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    tipos_examen = models.ManyToManyField(TipoExamen, related_name='examen_tiposexamen', null=True, blank=True)

    def __unicode__(self):
        return str(self.paciente)


class ImpresionDiagnostico(models.Model):
    class Meta:
        verbose_name = ('ImpresionDiagnostico')
        verbose_name_plural = ('ImpresionDiagnosticos')

    examen = models.ForeignKey(Examen, related_name='examen_impresion')
    diagnostico = models.ManyToManyField(DiagnosticoExamen, related_name='diagnosticos_impresion')

    def __unicode__(self):
        return self.diagnostico


class ResultadoItem(models.Model):
    class Meta:
        verbose_name = ('ResultadoItem')
        verbose_name_plural = ('Resultados Items')

    item = models.ForeignKey(ItemExamen, related_name='item_resultadoitem')
    examen= models.ForeignKey(Examen, related_name='examen_resultadoitem')
    texto = models.TextField()

    def __unicode__(self):
        return self.texto


class ResultadoSubItem(models.Model):
    class Meta:
        verbose_name = ('ResultadoSubItem')
        verbose_name_plural = ('Resultados SubItems')

    subitem = models.ForeignKey(SubItemExamen, related_name='item_resultadosubitem')
    examen= models.ForeignKey(Examen, related_name='examen_resultadosubitem')
    texto = models.TextField()

    def __unicode__(self):
        return self.texto
