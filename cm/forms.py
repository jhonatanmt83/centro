from django import forms
from cm.models import Perfil, Paciente, Paquete, Antecedente
from django.contrib.auth.models import Group
from django.forms.extras.widgets import SelectDateWidget
from django.forms import TextInput, CheckboxInput

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
            'fechanacimiento': TextInput(attrs={"class":"fecha_bonita"}),
        }
        
    

class PacienteForm2(forms.ModelForm):
    fecha_actual = forms.DateField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Paciente
        fields = ['nrohistoria', 'edadfur', 'null_edadfur', 'ultimofur', 'null_ultimofur', 'fecha_actual']
        widgets={
            "edadfur":TextInput(attrs={'class':'fecha_fur'}),
            "ultimofur":TextInput(attrs={'class':'fecha_finfur'}),
            "null_edadfur":CheckboxInput(attrs={'onClick':'desactivar_edadfur();'}),
            "null_ultimofur":CheckboxInput(attrs={'onClick':'desactivar_ultimofur();'}),

        }


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        widgets = {
            "edadfur":TextInput(attrs={'class':'fecha_fur'}),
            "ultimofur":TextInput(attrs={'class':'fecha_finfur'}),
            'fechanacimiento': TextInput(attrs={"class":"fecha_bonita"}),

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
