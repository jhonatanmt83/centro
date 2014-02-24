# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Paciente(models.Model):
    class Meta:
        verbose_name = ('Paciente')
        verbose_name_plural = ('Pacientes')

    dni = models.CharField(max_length=8, verbose_name=u'DNI', unique=True)
    nombres = models.CharField(max_length=200, verbose_name=u'Nombres y Apellidos')
    direccion = models.CharField(max_length=200, verbose_name=u'Dirección')
    edad = models.IntegerField(verbose_name=u'Edad')
    fechanacimiento = models.DateField(verbose_name=u'Fecha de Nacimiento')
    telefono = models.CharField(max_length=9, verbose_name=u'Teléfono')
    nrohistoria = models.CharField(max_length=6, verbose_name=u'N° de Historia Clínica', unique=True)
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

    personales = models.CharField(max_length=200, verbose_name=u'Personales', null=True, blank=True)
    familiares = models.CharField(max_length=200, verbose_name=u'Familiares', null=True, blank=True)
    cancer = models.CharField(max_length=200, verbose_name=u'Cancer', null=True, blank=True)
    otros = models.CharField(max_length=200, verbose_name=u'Otros', null=True, blank=True)
    examen = models.ForeignKey('Examen')

    def __unicode__(self):
        return str(self.examen)

class UltimaCita(models.Model):
    class Meta:
        verbose_name = ('UltimaCita')
        verbose_name_plural = ('UltimasCitas')

    paciente = models.ForeignKey(Paciente)
    proximo = models.DateField(verbose_name=u'Próxima cita')
    anterior = models.DateField(verbose_name=u'Última cita')

    def __unicode__(self):
        return unicode(str(self.paciente), 'utf8')


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

# class TipoCantidad(models.Model):
#     class Meta:
#         verbose_name = ('TipoCantidad')
#         verbose_name_plural = ('TipoCantidades')

#     nombre = models.CharField(max_length=100, verbose_name=u'Nombre')

#     def __unicode__(self):
#         return self.nombre

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

    nombre = models.CharField(max_length=100, verbose_name=u'Nombre Generico')
    nombre_comer = models.CharField(max_length=100, verbose_name=u'Nombre Comercial')
    clase = models.ForeignKey(ClaseMedicamento, verbose_name=u'Clase de Medicamento', related_name='medicamento_clase')
    #cantidad = models.ForeignKey(TipoCantidad, verbose_name=u'Tipode Cantidad', related_name='medicamento_cantidad')

    def __unicode__(self):
        return self.nombre


class Receta(models.Model):
    class Meta:
        verbose_name = ('Receta')
        verbose_name_plural = ('Recetas')

    paciente = models.ForeignKey(Paciente, verbose_name=u'Paciente')
    fecha = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return unicode(str(self.paciente), 'utf8')

    def obtener_diagnostico(self):
        return DiagnosticoxReceta.objects.filter(receta=self)[0]


class DiagnosticoxReceta(models.Model):
    class Meta:
        verbose_name = ('Diagnostico por Receta')
        verbose_name_plural = ('Diagnosticos por Recetas')

    receta = models.ForeignKey(Receta, verbose_name=u'Receta')
    diagnosticos = models.ManyToManyField(DiagnosticoReceta, verbose_name=u'Diagnósticos')

    def __unicode__(self):
        return str(self.receta)


class Tratamiento(models.Model):
    class Meta:
        verbose_name = ('Tratamiento')
        verbose_name_plural = ('Tratamientos')

    tipo_duracion = (
        ('di', 'Dias'),
        ('se', 'Semanas'),
        ('me', 'Meses'),
    )
    receta = models.ForeignKey(Receta, verbose_name=u'Receta')
    medicamento = models.ForeignKey(Medicamento, verbose_name=u'Medicamento', related_name='tratamiento_medicamento')
    cantidad = models.IntegerField(verbose_name=u'Cantidad')
    cantidaddosis = models.IntegerField(verbose_name=u'Cantidad de dosis')
    frecuencia = models.ForeignKey(Frecuencia, verbose_name=u'Frecuencia', related_name='tratamiento_frecuencia')
    duracion = models.IntegerField(verbose_name=u'Duración')
    tipoduracion = models.CharField(max_length=2,
                                    choices=tipo_duracion,
                                    default='di')

    def __unicode__(self):
        return str(self.receta)


BOOL_CHOICES = ((True, 'Pago de Personal'), (False, 'Otros pagos'))
class Egreso(models.Model):
    class Meta:
        verbose_name = ('Egreso')
        verbose_name_plural = ('Egresos')

    usuario = models.ForeignKey(User, verbose_name=u'Usuario')
    monto = models.DecimalField(max_digits=6, decimal_places=2)
    descripcion = models.TextField(verbose_name=u'Descripción')
    dni = models.CharField(max_length=8, verbose_name=u'DNI')
    fecha = models.DateField(auto_now_add=True)
    pagouotro = models.BooleanField('tipode pago',choices=BOOL_CHOICES)

    def __unicode__(self):
        return str(self.usuario)

    def obtenerdni(self):
        dni = Perfil.objects.filter(usuario = self.usuario)[0].dni
        return dni



#Para la parte de los exmanes

class TipoExamen(models.Model):
    class Meta:
        verbose_name = ('Tipo de Examen')
        verbose_name_plural = ('Tipos de Examenes')

    nombre = models.CharField(max_length=100, verbose_name=u'Nombre')
    subtitulo = models.CharField(max_length=200)
    descripcion = models.TextField(verbose_name=u'Descripción')
    fechacreacion = models.DateField(auto_now_add=True)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre

#     def obtener_items(self):
#         return ItemExamen.objects.filter(tipoexamen=self)
    

# class ItemExamen(models.Model):
#     class Meta:
#         verbose_name = ('ItemExamen')
#         verbose_name_plural = ('ItemsExamenes')

#     texto = models.CharField(max_length=100, verbose_name=u'Texto')
#     tipoexamen = models.ForeignKey(TipoExamen)

#     def __unicode__(self):
#         return self.texto

#     def obtener_subitems(self):
#         return SubItemExamen.objects.filter(item=self)

#     def obtener_opciones(self):
#         return OpcionItem.objects.filter(item=self)


# class SubItemExamen(models.Model):
#     class Meta:
#         verbose_name = ('SubItemExamen')
#         verbose_name_plural = ('SubItemsExamenes')

#     texto = models.CharField(max_length=100, verbose_name=u'Texto')
#     item = models.ForeignKey(ItemExamen)

#     def __unicode__(self):
#         return self.texto

#     def obtener_opciones(self):
#         return OpcionSubItem.objects.filter(subitem=self)


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
        retornar = 0
        examenes = self.tiposexamen.all()
        for examen in examenes:
            retornar +=examen.precio
        return retornar


class Examen(models.Model):
    class Meta:
        verbose_name = ('Examen')
        verbose_name_plural = ('Examenes')

    paciente = models.ForeignKey(Paciente, related_name='examen_paciente')
    paquetes = models.ManyToManyField(Paquete, related_name='examen_paquetes', null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)
    fecha_editado = models.DateField(auto_now=True)
    recomendaciones = models.TextField(null=True, blank=True)
    terminado = models.BooleanField(default=False)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    tipos_examen = models.ManyToManyField(TipoExamen, related_name='examen_tiposexamen', null=True, blank=True)

    def __unicode__(self):
        unicode(str(self.paciente), 'utf8')

    def obtnerpaquete(self):
        nombpaquete=self.paquetes.all()[0]
        return nombpaquete.nombre


class ImpresionDiagnostico(models.Model):
    class Meta:
        verbose_name = ('ImpresionDiagnostico')
        verbose_name_plural = ('ImpresionDiagnosticos')

    examen = models.ForeignKey(Examen, related_name='examen_impresion')
    diagnostico = models.ManyToManyField(DiagnosticoExamen, related_name='diagnosticos_impresion')

    def __unicode__(self):
        return str(self.examen)


# class OpcionItem(models.Model):
#     class Meta:
#         verbose_name = ('OpcionItem')
#         verbose_name_plural = ('OpcionItems')

#     item = models.ForeignKey(ItemExamen)
#     texto = models.CharField(max_length=200)

#     def __unicode__(self):
#         return self.texto


# class OpcionSubItem(models.Model):
#     class Meta:
#         verbose_name = ('OpcionSubItem')
#         verbose_name_plural = ('OpcionSubItems')

#     subitem = models.ForeignKey(SubItemExamen)
#     texto = models.CharField(max_length=200)

#     def __unicode__(self):
#         return self.texto

    
# class ResultadoItem(models.Model):
#     class Meta:
#         verbose_name = ('ResultadoItem')
#         verbose_name_plural = ('Resultados Items')

#     item = models.ForeignKey(ItemExamen, related_name='item_resultadoitem')
#     examen= models.ForeignKey(Examen, related_name='examen_resultadoitem')
#     seleccionados = models.ManyToManyField(OpcionItem, related_name='seleccionados_resultadoitem')

#     def __unicode__(self):
#         return self.texto


# class ResultadoSubItem(models.Model):
#     class Meta:
#         verbose_name = ('ResultadoSubItem')
#         verbose_name_plural = ('Resultados SubItems')

#     subitem = models.ForeignKey(SubItemExamen, related_name='item_resultadosubitem')
#     examen= models.ForeignKey(Examen, related_name='examen_resultadosubitem')
#     seleccionados = models.ManyToManyField(OpcionSubItem, related_name='seleccionados_resultadosubitem')

#     def __unicode__(self):
#         return self.texto


#perfil personal

class Perfil(models.Model):
    class Meta:
        verbose_name = ('Perfil')
        verbose_name_plural = ('Perfiles')

    usuario = models.ForeignKey(User)
    dni = models.CharField(max_length=8, verbose_name=u'DNI')
    nombres = models.CharField(max_length=200, verbose_name=u'Nombres y Apellidos')
    profesion = models.CharField(max_length=200, verbose_name=u'Profesión', blank=True, null=True)
    direccion = models.CharField(max_length=200, verbose_name=u'Dirección', blank=True, null=True)
    sueldo = models.DecimalField(max_digits=6, decimal_places=2)

    def __unicode__(self):
        return str(self.usuario)


# Nuevos Examenes

# class Item(models.Model):
#     class Meta:
#         verbose_name = ('Item')
#         verbose_name_plural = ('Items')

#     CAMPOS = (
#         ('01', 'utero_eg'),
#         ('02', 'situac_eg'),
#         ('03', 'pres_eg'),
#         ('04', 'dorso_eg'),
#         ('05', 'actcard_eg'),
#         ('06', 'crl_eg'),
#         ('07', 'dbp_eg'),
#         ('08', 'cabeza_eg'),
#         ('09', 'corazon_eg'),
#         ('10', 'abdomen_eg'),
#         ('11', 'genitales_eg'),
#         ('12', 'extrem_eg'),
#         ('13', 'cordon_eg'),
#         ('14', 'placenta_eg'),
#         ('15', ''),
#         ('', ''),
#     )

#     texto = models.TextField(verbose_name=u'Texto')
#     tipo_examen = models.ForeignKey(TipoExamen)
#     campo = models.CharField(max_length=2, choices=CAMPOS)

#     def __unicode__(self):
#         return self.texto
    


# class EcografiaGenetica(models.Model):
#     class Meta:
#         verbose_name = ('EcografiaGenetica')
#         verbose_name_plural = ('EcografiaGeneticas')

#     # Hallazgos
#     utero = models.ManyToManyField(Item, related_name='utero_eg', blank=True, null=True)
#     situac = models.ManyToManyField(Item, related_name='situac_eg', blank=True, null=True)
#     pres = models.ManyToManyField(Item, related_name='pres_eg', blank=True, null=True)
#     dorso = models.ManyToManyField(Item, related_name='dorso_eg', blank=True, null=True)
#     actcard = models.ManyToManyField(Item, related_name='actcard_eg', blank=True, null=True, verbose_name=u'Act/Card')
#     crl = models.ManyToManyField(Item, related_name='crl_eg', blank=True, null=True)
#     dbp = models.ManyToManyField(Item, related_name='dbp_eg', blank=True, null=True)
#     # Anatomia Fetal
#     cabeza = models.ManyToManyField(Item, related_name='cabeza_eg', blank=True, null=True)
#     corazon = models.ManyToManyField(Item, related_name='corazon_eg', blank=True, null=True)
#     abdomen = models.ManyToManyField(Item, related_name='abdomen_eg', blank=True, null=True)
#     genitales = models.ManyToManyField(Item, related_name='genitales_eg', blank=True, null=True)
#     extrem = models.ManyToManyField(Item, related_name='extrem_eg', blank=True, null=True)
#     cordon = models.ManyToManyField(Item, related_name='cordon_eg', blank=True, null=True)
#     placenta = models.ManyToManyField(Item, related_name='placenta_eg', blank=True, null=True)

#     def __unicode__(self):
#         return str(self.pk)


# class EcografiaObstetrica(models.Model):
#     class Meta:
#         verbose_name = ('EcografiaObstetrica')
#         verbose_name_plural = ('EcografiasObstetricas')

#     # Hallazgos
#     utero = models.ManyToManyField(Item, related_name='utero_eo', blank=True, null=True)

#     def __unicode__(self):
#         pass
#     


