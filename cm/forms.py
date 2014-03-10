from django import forms


from cm.models import Perfil, Paciente, Paquete, Antecedente, Egreso, DiagnosticoReceta, DiagnosticoxReceta
from cm.models import ClaseMedicamento, Medicamento, Frecuencia, Tratamiento, UltimaCita

from django.contrib.auth.models import Group
from django.forms.extras.widgets import SelectDateWidget
from django.forms import TextInput, CheckboxInput, Select


from datetime import date

#funciones
def ObtenerPaquetes():
    paquetes_total = Paquete.objects.all()
    seleccionado = []
    for paquete in paquetes_total:
        seleccionado.append((str(paquete.pk), paquete.nombre))
    seleccionado = tuple(seleccionado)
    return seleccionado

# endfunciones


class PerfilForm(forms.ModelForm):
    rol = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label=None)

    class Meta:
        model = Perfil
        exclude = ['usuario']


class PacienteForm1(forms.ModelForm):
    edad = forms.IntegerField(label="Edad", widget=forms.TextInput(attrs={'readonly': 'readonly'}))

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
            "nrohistoria":TextInput(attrs={'readonly': 'readonly'}),
            "edadfur":TextInput(attrs={'class':'fecha_fur'}),
            "ultimofur":TextInput(attrs={'class':'fecha_finfur'}),
            "null_edadfur":CheckboxInput(attrs={'onClick':'desactivar_edadfur();'}),
            "null_ultimofur":CheckboxInput(attrs={'onClick':'desactivar_ultimofur();'}),

        }


class PacienteForm(forms.ModelForm):
    edad = forms.IntegerField(label="Edad", widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Paciente
        fields = ['dni', 'nombres', 'direccion', 'edad', 'fechanacimiento', 'telefono', 'nrohistoria', 'edadfur', 'null_edadfur', 'ultimofur', 'null_ultimofur']
        widgets = {
            "edadfur":TextInput(attrs={'class':'fecha_fur'}),
            "ultimofur":TextInput(attrs={'class':'fecha_finfur'}),
            'fechanacimiento': TextInput(attrs={"class":"fecha_bonita"}),
            "nrohistoria":TextInput(attrs={'readonly': 'readonly'}),
        }


class PaquetesSeleccionForm(forms.Form):
    paquetes = forms.MultipleChoiceField(required=True,
        widget=forms.CheckboxSelectMultiple, choices=ObtenerPaquetes())


class AntecedenteForm(forms.ModelForm):
    class Meta:
        model = Antecedente
        exclude = ['examen']


class EgresoForm(forms.ModelForm):
    class Meta:
        model = Egreso
        fields = ['pagouotro','dni', 'usuario', 'monto', 'descripcion',]
        ecogepago=((True, 'Pago de Personal'),(False,'Otros pagos'))
        widgets = {
            'pagouotro': forms.RadioSelect
        }
 

class CitaForm(forms.ModelForm):
    class Meta:
        model= UltimaCita
        exclude =['paciente','anterior']


class DiagnosticoxRecetaForm(forms.ModelForm):
    class Meta:
        model = DiagnosticoxReceta
        widgets = {
            'diagnosticos': forms.CheckboxSelectMultiple,
        }
        exclude = ['receta',]


class TratamientoM1Form(forms.ModelForm):
    tipomedicamento = forms.ModelChoiceField(queryset=ClaseMedicamento.objects.all(), empty_label="Seleccione tipo", widget=forms.Select(attrs={'onchange':'actualizar_medicamentos()', 'class':'form-control'}), label='Tipo')
    class Meta:
        model = Tratamiento
        exclude = ['receta', 'cantidaddosis', 'frecuencia', 'duracion', 'tipoduracion', 'posologia']
        fields = ['tipomedicamento', 'medicamento', 'cantidad']
        widgets = {
            'medicamento': Select(attrs={'class': 'form-control'}),
            'cantidad': TextInput(attrs={'class': 'form-control'}),
        }


class TratamientoM2Form(forms.ModelForm):
    class Meta:
        model = Tratamiento
        fields = ['cantidaddosis', 'frecuencia', 'duracion', 'tipoduracion', 'posologia']
        exclude = ['receta', 'tipomedicamento', 'medicamento', 'cantidad']
        widgets = {
            'cantidaddosis': TextInput(attrs={'class': 'form-control'}),
            'frecuencia': Select(attrs={'class': 'form-control'}),
            'duracion': TextInput(attrs={'class': 'form-control'}),
            'tipoduracion': Select(attrs={'class': 'form-control'}),
            'posologia': TextInput(attrs={'class': 'form-control'}),
        }


class TratamientoForm(forms.ModelForm):
    tipomedicamento = forms.ModelChoiceField(queryset=ClaseMedicamento.objects.all(), empty_label="Seleccione tipo", widget=forms.Select(attrs={'onchange':'actualizar_medicamentos()'}))
    class Meta:
        model = Tratamiento
        exclude = ['receta']
        fields = ['tipomedicamento', 'medicamento', 'cantidad', 'cantidaddosis', 'frecuencia', 'duracion', 'tipoduracion', 'posologia']


class DiagnosticoRecetaForm(forms.ModelForm):
    class Meta:
        model = DiagnosticoReceta
