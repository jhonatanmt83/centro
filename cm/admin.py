from django.contrib import admin

# Register your models here.
from cm.models import Paciente, Antecedente, UltimaCita, DiagnosticoExamen, ClaseMedicamento, TipoCantidad, Frecuencia, Medicamento, Receta, DiagnosticoReceta, Tratamiento, Egreso, TipoExamen, ItemExamen, SubItemExamen, Paquete, Examen, ImpresionDiagnostico, ResultadoItem, ResultadoSubItem, Perfil


admin.site.register(Paciente)
admin.site.register(Antecedente)
admin.site.register(UltimaCita)
admin.site.register(DiagnosticoExamen)
admin.site.register(ClaseMedicamento)
admin.site.register(TipoCantidad)
admin.site.register(Frecuencia)
admin.site.register(Medicamento)
admin.site.register(Receta)
admin.site.register(DiagnosticoReceta)
admin.site.register(Tratamiento)
admin.site.register(Egreso)
admin.site.register(TipoExamen)
admin.site.register(ItemExamen)
admin.site.register(SubItemExamen)
admin.site.register(Paquete)
admin.site.register(Examen)
admin.site.register(ImpresionDiagnostico)
admin.site.register(ResultadoItem)
admin.site.register(ResultadoSubItem)
admin.site.register(Perfil)