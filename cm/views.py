#-*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.template import RequestContext

from centro.decoratos import registrador_login, evaluador_login, administrador_login
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden

from cm.forms import PerfilForm, PacienteForm1, PacienteForm2, PaquetesSeleccionForm, AntecedenteForm, PacienteForm
from django.contrib.auth.models import User, Group

from cm.models import Perfil, Paquete, Examen, Antecedente, DiagnosticoExamen, ImpresionDiagnostico, UltimaCita, Egreso, Receta



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
    
    egreso = Egreso.objects.all()
    valor={'examenes':examenes,'egreso':egreso}

    return render_to_response('administrador/caja.html',valor, context_instance=RequestContext(request))



@administrador_login
def recetas(request):
    receta = Receta.objects.all()
    

    return render_to_response('administrador/recetas.html',{'receta':receta}, context_instance=RequestContext(request))

