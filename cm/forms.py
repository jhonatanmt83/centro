from django import forms
from cm.models import Perfil, Paciente, Paquete, Antecedente
from django.contrib.auth.models import Group
from django.forms.extras.widgets import SelectDateWidget

from datetime import date



class PerfilForm(forms.ModelForm):
    rol = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label=None)

    class Meta:
        model = Perfil
        exclude = ['usuario']


class PacienteForm1(forms.ModelForm):

    class Meta:
        model = Paciente
        fields = ['dni', 'nombres', 'direccion', 'edad', 'fechanacimiento', 'telefono']
        widgets = {
            'fechanacimiento': SelectDateWidget(),
        }
        
    

class PacienteForm2(forms.ModelForm):
    fecha_actual = forms.DateField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Paciente
        fields = ['nrohistoria', 'edadfur', 'null_edadfur', 'ultimofur', 'null_ultimofur', 'fecha_actual']


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        widgets = {
            'fechanacimiento': SelectDateWidget(years=range(1960,2014)),
        }
    

paquetes_total = Paquete.objects.all()
seleccionado = []
for paquete in paquetes_total:
    seleccionado.append((str(paquete.pk), paquete.nombre))
seleccionado = tuple(seleccionado)

class PaquetesSeleccionForm(forms.Form):
    paquetes = forms.MultipleChoiceField(required=True,
        widget=forms.CheckboxSelectMultiple, choices=seleccionado)


class AntecedenteForm(forms.ModelForm):
    class Meta:
        model = Antecedente
        exclude = ['examen']
