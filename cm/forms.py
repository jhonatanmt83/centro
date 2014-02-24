from django import forms
from cm.models import Perfil, Paciente, Paquete, Antecedente, Egreso, DiagnosticoReceta, DiagnosticoxReceta
from cm.models import ClaseMedicamento, Medicamento, Frecuencia, Tratamiento
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



# class egreso_formulario(forms.ModelForm):

#     dni         =forms.CharField(widget=forms.TextInput())
#     nombre      =forms.CharField(widget=forms.TextInput())
#     monto       =forms.CharField(widget=forms.TextInput())
#     decripciion =forms.CharField(widget=forms.Textarea())

class EgresoForm(forms.ModelForm):
    class Meta:
        model = Egreso
        fields = ['pagouotro','dni', 'usuario', 'monto', 'descripcion',]
        ecogepago=((True, 'Pago de Personal'),(False,'Otros pagos'))
        widgets = {
            'pagouotro': forms.RadioSelect
        }
        

class DiagnosticoxRecetaForm(forms.ModelForm):
    class Meta:
        model = DiagnosticoxReceta
        widgets = {
            'diagnosticos': forms.CheckboxSelectMultiple,
        }
        exclude = ['receta',]


class Tratamiento1Form(forms.Form):
    tipomedicamento = forms.ModelChoiceField(queryset=ClaseMedicamento.objects.all(), empty_label=None)
    medicamento = forms.ModelChoiceField(queryset=Medicamento.objects.all(), empty_label=None)
    cantidad = forms.IntegerField(label="Cantidad")


class Tratamiento2Form(forms.Form):
    tipo_duracion = (
        ('di', 'Dias'),
        ('se', 'Semanas'),
        ('me', 'Meses'),
    )
    dosis = forms.IntegerField(label="Dosis")
    frecuencia = forms.ModelChoiceField(queryset=Frecuencia.objects.all(), empty_label=None)
    duracion = forms.IntegerField(label="Durante")
    tipo_duracion = forms.ChoiceField(choices=tipo_duracion)

class TratamientoM1Form(forms.ModelForm):
    tipomedicamento = forms.ModelChoiceField(queryset=ClaseMedicamento.objects.all(), empty_label=None)
    class Meta:
        model = Tratamiento
        exclude = ['receta', 'cantidaddosis', 'frecuencia', 'duracion', 'tipoduracion']
        fields = ['tipomedicamento', 'medicamento', 'cantidad']


class TratamientoM2Form(forms.ModelForm):
    class Meta:
        model = Tratamiento
        fields = ['cantidaddosis', 'frecuencia', 'duracion', 'tipoduracion']
        exclude = ['receta', 'tipomedicamento', 'medicamento', 'cantidad']


class TratamientoForm(forms.ModelForm):
    class Meta:
        model = Tratamiento
        exclude = ['receta']


class DiagnosticoRecetaForm(forms.ModelForm):
    class Meta:
        model = DiagnosticoReceta
    