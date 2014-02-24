#-*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.template import RequestContext

from django.db.models import Sum


from centro.decoratos import registrador_login, evaluador_login, administrador_login
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden


from cm.forms import PerfilForm, PacienteForm1, PacienteForm2, PaquetesSeleccionForm, AntecedenteForm, PacienteForm, EgresoForm
from cm.forms import DiagnosticoxRecetaForm, Tratamiento1Form, Tratamiento2Form, TratamientoM1Form, TratamientoM2Form
from cm.forms import TratamientoForm, DiagnosticoRecetaForm, CitaForm
from cm.forms import DiagnosticoxRecetaForm

from django.contrib.auth.models import User, Group

from cm.models import Perfil, Paquete, Examen, Antecedente, DiagnosticoExamen, ImpresionDiagnostico, UltimaCita, Egreso, Receta, Paciente
from cm.models import DiagnosticoxReceta, DiagnosticoReceta, Tratamiento

from django.shortcuts import get_object_or_404


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
    paquetes = Paquete.objects.all()
    fecha_actual = str(date.today().day) + "/" + str(date.today().month) + "/" + str(date.today().year)
    if request.method=='POST':
        formulario1 = PacienteForm1(request.POST)
        formulario2 = PacienteForm2(request.POST)
        formulario_paciente = PacienteForm(request.POST)
        paquetesform = PaquetesSeleccionForm(request.POST)
        antecedentesform = AntecedenteForm(request.POST)
        if formulario_paciente.is_valid() and antecedentesform.is_valid() and paquetesform.is_valid():
            paciente = formulario_paciente.save()
            lista_paquetes = []
            lista_seleccionados = paquetesform.cleaned_data.get('paquetes')
            for elemento in lista_seleccionados:
                lista_paquetes.append(Paquete.objects.get(pk=int(elemento)))
            examen = Examen(paciente=paciente, recomendaciones='', terminado=False, precio=request.POST['precio_total'])
            examen.save()
            examen.paquetes = lista_paquetes
            instancia = Antecedente(examen=examen)
            antecedente = AntecedenteForm(request.POST, instance=instancia)
            antecedente.save()
            receta = Receta(paciente=paciente)
            receta.save()
            diagxreceta = DiagnosticoxReceta(receta=receta)
            diagxreceta.save()
            messages.success(request, 'Nuevo paciente %s creado'% (request.POST['nombres']))
            # Nuevos formularios
            formulario1 = PacienteForm1
            formulario2 = PacienteForm2(initial={'fecha_actual': fecha_actual})
            paquetesform = PaquetesSeleccionForm
            antecedentesform = AntecedenteForm
    else:
        formulario1 = PacienteForm1
        formulario2 = PacienteForm2(initial={'fecha_actual': fecha_actual})
        paquetesform = PaquetesSeleccionForm
        antecedentesform = AntecedenteForm
    return render_to_response('administrador/nuevo_paciente.html', {'formulario1': formulario1, 'formulario2': formulario2, 'paquetesform': paquetesform, 'antecedentesform': antecedentesform, 'paquetes': paquetes}, context_instance=RequestContext(request))


@administrador_login
def examen(request, codigo):
    examen = Examen.objects.get(pk=codigo)
    antecedente = Antecedente.objects.filter(examen=examen)[0]
    if request.method=='POST':
        for paquete in examen.paquetes.all():
            for tipo_examen in paquete.tiposexamen.all():
                items = tipo_examen.obtener_items()
                for item in items:
                    if item.obtener_subitems():
                        subitems = item.obtener_subitems()
                        for subitem in subitems:
                            subitem_resultado = ResultadoSubItem(subitem=subitem, examen=examen, texto=request.POST['item_'+str(subitem.pk)])
                            subitem_resultado.save()
                    else:
                        item_resultado = ResultadoItem(item=item, examen=examen, texto=request.POST['item_'+str(item.pk)])
                        item_resultado.save()
        diagnosticos_add = []
        for numero_diagnostico in range(1,int(request.POST['num_diagnosticos'])+1):
            if (request.POST['diagnostico_'+str(numero_diagnostico)] != ""):
                nuevo_diagnostico = DiagnosticoExamen(texto=request.POST['diagnostico_'+str(numero_diagnostico)])
                nuevo_diagnostico.save()
                diagnosticos_add.append(nuevo_diagnostico)
        nueva_impresion = ImpresionDiagnostico(examen=examen)
        nueva_impresion.save()
        nueva_impresion.diagnostico = diagnosticos_add
        examen.recomendaciones = request.POST['recomendaciones']
        examen.terminado = True
        examen.save()
        cita = UltimaCita.objects.filter(paciente=examen.paciente)
        fecha_new = request.POST['proxima_cita'].split("/")
        if not cita:
            new_cita = UltimaCita(paciente=examen.paciente, proximo=date(int(fecha_new[2]), int(fecha_new[0]), int(fecha_new[1])), anterior=date.today())
            new_cita.save()
        else:
            temp_cita = cita.proximo
            cita.anterior = temp_cita
            cita.proximo = date(int(fecha_new[2]), int(fecha_new[0]), int(fecha_new[1]))
            cita.save()
    else:
        pass
    return render_to_response('administrador/examen.html', {'antecedente':antecedente, 'examen':examen}, context_instance=RequestContext(request))


# Function json
def precio_paquete(request, codigo):
    """Devuelve el precio correspondiente al paquete"""
    paquete = Paquete.objects.get(pk=int(codigo))
    new_result = []
    datos = {}
    datos['precio'] = str(paquete.precio_total())
    new_result.append(datos)
    return HttpResponse(json.dumps(new_result))


def resultado_impresiones(request):
 
    #if request.method=='GET' or not request.POST.__contains__('start'):
    #    return HttpResponseForbidden()
 
    # Hacemos la consulta para aquellos elementos que empiecen por start ordenados por nombre
    print "inicio"
    query = DiagnosticoExamen.objects.filter(texto__istartswith=request.POST['start']).order_by('texto')
    print query
    # Serializamos
    objects = u'{items: [\n'
    for i in query:
        objects += u'{"0":"%s"},\n' % (i.texto.replace('"',''))
    objects=objects.strip(",\n");
    objects+=u']}\n'
    print objects
 
    return HttpResponse(objects,mimetype="text/plain")


@administrador_login
def citas(request):
    cita = UltimaCita.objects.all()

    return render_to_response('administrador/citas.html',{'cita':cita}, context_instance=RequestContext(request))


@administrador_login
def examenescaja(request):
    examenes = Examen.objects.filter(fecha = date.today())
    
    egreso = Egreso.objects.filter(fecha=date.today())
    
    suma_egreso=egreso.aggregate(Sum('monto'))
    suma_ingreso=examenes.aggregate(Sum('precio'))
    if not egreso: 
        sumar_egreso=0
    else:
        sumar_egreso=suma_egreso['monto__sum']
    if not examenes: 
        sumar_ingreso=0
    else:
        sumar_ingreso=suma_ingreso['precio__sum']
    resta = sumar_ingreso - sumar_egreso
    valor={'examenes':examenes,'egreso':egreso,'sumaegreso':suma_egreso,'sumaingreso':suma_ingreso, 'resta': resta}
    return render_to_response('administrador/caja.html',valor, context_instance=RequestContext(request))



@administrador_login
def recetas(request):
    recetas = Receta.objects.all()
    return render_to_response('administrador/recetas.html',{'recetas':recetas}, context_instance=RequestContext(request))

@administrador_login

def historiaclinica(request, codigo):
    historiaclinica = Paciente.objects.filter(nrohistoria=codigo)
    if historiaclinica:
        historiaclinica=historiaclinica[0]

    return render_to_response('administrador/historiaclinica.html', {'historiaclinicas':historiaclinica}, context_instance=RequestContext(request))


@administrador_login
def lista_historia_clinica(request):
    lista_clinica = Paciente.objects.all()
    lista={'listahistoria':lista_clinica}
    return render_to_response('administrador/listahistoriaclinica.html',lista, context_instance=RequestContext(request))


@administrador_login
def receta_diagnostico(request, codigo):
    cerrar = False
    receta = get_object_or_404(Receta, pk=codigo)
    instancia = receta.obtener_diagnostico()
    form = DiagnosticoxRecetaForm(request.POST or None, instance=instancia)
    if form.is_valid():
        form.save()
        cerrar = True
    return render_to_response('administrador/receta_diagnostico.html',{'form': form, 'cerrar': cerrar},context_instance=RequestContext(request))


@administrador_login
def receta_tratamiento(request, codigo):
    receta = Receta.objects.get(pk=codigo)
    if request.method=='POST':
        instancia = Tratamiento(receta=receta)
        formulario = TratamientoForm(request.POST, instance=instancia)
        form1 = TratamientoM1Form(request.POST)
        form2 = TratamientoM2Form(request.POST)
        if formulario.is_valid():
            formulario.save()
            form1 = TratamientoM1Form()
            form2 = TratamientoM2Form()
        else:
            print "error"
        tratamientos = Tratamiento.objects.filter(receta=receta)
    else:
        form1 = TratamientoM1Form()
        form2 = TratamientoM2Form()
        tratamientos = Tratamiento.objects.filter(receta=receta)
    return render_to_response('administrador/receta_tratamiento.html',{'form1': form1, 'form2': form2, 'tratamientos': tratamientos},context_instance=RequestContext(request))


@administrador_login
def receta_modificar(request, codigo):
    receta = Receta.objects.get(pk=codigo)
    tratamientos = Tratamiento.objects.filter(receta=receta)
    diagnosticos = receta.obtener_diagnostico()
    return render_to_response('administrador/receta_modificar.html',{'tratamientos': tratamientos, 'diagnosticos': diagnosticos, 'receta': receta},context_instance=RequestContext(request))


@administrador_login
def receta_modificar_tratamiento(request, id_receta, id_tratamiento):
    instancia = get_object_or_404(Tratamiento, pk=id_tratamiento)
    receta = Receta.objects.get(pk=id_receta)
    tratamiento = Tratamiento.objects.get(pk=id_tratamiento)
    formulario = TratamientoForm(request.POST or None, instance=tratamiento)
    if formulario.is_valid():
        formulario.save()
        return HttpResponseRedirect("/administrador/receta/modificar/"+str(id_receta))
    return render_to_response('administrador/receta_modificar_tratamiento.html',{'formulario': formulario},context_instance=RequestContext(request))


@administrador_login
def receta_modificar_diagnostico(request, id_receta, id_diagnostico):
    receta = Receta.objects.get(pk=id_receta)
    diagnostico = DiagnosticoReceta.objects.get(pk=id_diagnostico)
    formulario = DiagnosticoRecetaForm(request.POST or None, instance=diagnostico)
    if formulario.is_valid():
        formulario.save()
        return HttpResponseRedirect("/administrador/receta/modificar/"+str(id_receta))
    return render_to_response('administrador/receta_modificar_diagnostico.html',{'formulario': formulario},context_instance=RequestContext(request))


@administrador_login
def receta_imprimir(request, codigo):
    receta=Receta.objects.get(pk=codigo)
    diagnosticos = receta.obtener_diagnostico()
    tratamientos = Tratamiento.objects.filter(receta=receta)
    cita = UltimaCita.objects.filter(paciente=receta.paciente).order_by('-pk')
    if cita:
        cita = cita[0]
    return render_to_response('administrador/receta_imprimir.html',{'receta_impresa': receta, 'diagnosticos':diagnosticos, 'tratamientos':tratamientos, 'cita': cita},context_instance=RequestContext(request))


def vista_egreso(request):
    if request.method == 'POST': # If the form has been submitted...
        form = EgresoForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            form.save()
            messages.success(request, 'monto de  %s Nuevos Soles generado '% (request.POST['monto']))
            form=EgresoForm()
    else:
        form = EgresoForm() # An unbound form
    formulario  =   EgresoForm()
    return render_to_response('administrador/egreso.html',{'formulario':formulario},context_instance=RequestContext(request))


def modi_historia_clinica(request, codigo):
    instancia = get_object_or_404(Paciente, pk=codigo)
    modificar = PacienteForm(request.POST or None, instance=instancia)
    if modificar.is_valid():
        modificar.save()
        messages.success(request, 'LOS CAMBIOS FUERON GUARDADOS CON ÉXITO ')

    return render_to_response('administrador/modificarhistoria.html', {'formhistoria': modificar}, context_instance=RequestContext(request))


def modificarcita(request, codigo):
    instancia = get_object_or_404(UltimaCita, pk=codigo)
    nueva_cita= CitaForm(request.POST or None, instance=instancia)
    
    if nueva_cita.is_valid():
        nueva_cita.save()
        messages.success(request, 'SU NUEVA CITA SERA EL %s '% (request.POST['proximo']))
     
    return render_to_response('administrador/modificarcita.html',{'nueva_cita':nueva_cita},context_instance=RequestContext(request))
    


def agregar_diagnostico(request):
    """Agrega nuevo diagnostico de receta"""
    texto = request.POST['texto']
    nuevo_diagnostico = DiagnosticoReceta(texto=texto)
    nuevo_diagnostico.save()
    new_result = []
    datos = {}
    datos['id'] = str(nuevo_diagnostico.pk)
    datos['texto'] = str(nuevo_diagnostico.texto)
    new_result.append(datos)
    return HttpResponse(json.dumps(new_result))


def eliminar_tratamiento(request):
    """Elimina el tratamiento"""
    tratamiento = Tratamiento.objects.get(pk=request.POST['eliminar'])
    tratamiento.delete()
    new_result = []
    datos = {}
    new_result.append(datos)
    return HttpResponse(json.dumps(new_result))


def quitar_diagnostico_receta(request):
    """Elimina el tratamiento"""
    diagnostico = DiagnosticoxReceta.objects.get(pk=request.POST['diagnostico'])
    diagnostico_receta = DiagnosticoReceta.objects.get(pk=request.POST['diagnosticoreceta'])
    diagnostico.diagnosticos.remove(diagnostico_receta)
    #diagnostico.save()
    
    new_result = []
    datos = {}
    new_result.append(datos)
    return HttpResponse(json.dumps(new_result))
