from django.contrib import admin

# Register your models here.
from cm.models import Paciente, Antecedente, UltimaCita, DiagnosticoExamen, ClaseMedicamento, Frecuencia, Medicamento, Receta, DiagnosticoReceta, Tratamiento, Egreso, TipoExamen, Paquete, Examen, ImpresionDiagnostico, Perfil, DiagnosticoxReceta
from cm.models import ItemExamen, SubItemExamen, TablaMedidas, OpcionItem, OpcionSubItem, ResultadoItem, ResultadoSubItem
from cm.models import Conclusion


admin.site.register(Paciente)
admin.site.register(Antecedente)
admin.site.register(UltimaCita)
admin.site.register(DiagnosticoExamen)
admin.site.register(ClaseMedicamento)
#admin.site.register(TipoCantidad)
admin.site.register(Frecuencia)
admin.site.register(DiagnosticoReceta)
admin.site.register(Medicamento)
admin.site.register(Receta)
admin.site.register(DiagnosticoxReceta)
admin.site.register(Tratamiento)
admin.site.register(Egreso)
admin.site.register(TipoExamen)
admin.site.register(ItemExamen)
admin.site.register(SubItemExamen)
admin.site.register(Paquete)
admin.site.register(TablaMedidas)
admin.site.register(Examen)
admin.site.register(ImpresionDiagnostico)
admin.site.register(OpcionItem)
admin.site.register(OpcionSubItem)
admin.site.register(ResultadoItem)
admin.site.register(ResultadoSubItem)
admin.site.register(Perfil)
admin.site.register(Conclusion)
