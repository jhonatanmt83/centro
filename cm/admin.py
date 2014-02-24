from django.contrib import admin

# Register your models here.
from cm.models import Paciente, Antecedente, UltimaCita, DiagnosticoExamen, ClaseMedicamento, Frecuencia, Medicamento, Receta, DiagnosticoReceta, Tratamiento, Egreso, TipoExamen, Paquete, Examen, ImpresionDiagnostico, Perfil, DiagnosticoxReceta


admin.site.register(Paciente)
admin.site.register(Antecedente)
admin.site.register(UltimaCita)
admin.site.register(DiagnosticoExamen)
admin.site.register(ClaseMedicamento)
#admin.site.register(TipoCantidad)
admin.site.register(Frecuencia)
admin.site.register(Medicamento)
admin.site.register(Receta)
admin.site.register(DiagnosticoReceta)
admin.site.register(Tratamiento)
admin.site.register(Egreso)
admin.site.register(TipoExamen)
admin.site.register(Paquete)
admin.site.register(Examen)
admin.site.register(ImpresionDiagnostico)
admin.site.register(Perfil)
admin.site.register(DiagnosticoxReceta)