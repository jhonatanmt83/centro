from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'centro.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'cm.views.home', name='home'),
    url(r'^login/$', 'django.contrib.auth.views.login',{'template_name':'login.html'}, name='login'),
    url(r'^cerrar/$', 'django.contrib.auth.views.logout_then_login', name='logout'),

    url(r'^registrador/$', 'cm.views.registrador', name='registrador'),
    url(r'^evaluador/$', 'cm.views.evaluador', name='evaluador'),
    url(r'^administrador/$', 'cm.views.administrador', name='administrador'),
    url(r'^administrador/usuario$', 'cm.views.nuevo_usuario', name='nuevo_usuario'),
    url(r'^administrador/paciente$', 'cm.views.nuevo_paciente', name='nuevo_paciente'),
    url(r'^administrador/citas$', 'cm.views.citas', name='citas'),
    url(r'^administrador/caja$', 'cm.views.examenescaja', name='caja'),
    url(r'^administrador/receta$', 'cm.views.recetas', name='recetas'),
    url(r'^administrador/examen/$', 'cm.views.examen_lista', name='examen_lista'),
    url(r'^administrador/examen/(?P<codigo>\d+)/$', 'cm.views.examen', name='examen'),
    url(r'^administrador/historiaclinica/(?P<codigo>\d+)/$', 'cm.views.historiaclinica', name='historiaclinica'),
    url(r'^administrador/listaclinica$', 'cm.views.lista_historia_clinica', name='lista_historia_clinica'),
    url(r'^administrador/egreso/$', 'cm.views.vista_egreso', name='egresos'),
    url(r'^administrador/modificarhistoria/(?P<codigo>\d+)/$', 'cm.views.modi_historia_clinica', name='modi_historia_clinica'),
    url(r'^administrador/modificarcita/(?P<codigo>\d+)/$', 'cm.views.modificarcita', name='nuevacita'),
    
    # Urls con json
    url(r'^precio/paquete/(?P<codigo>\d+)/$', 'cm.views.precio_paquete', name='precio_paquete'),
    url(r'^obtener/medicamentos/(?P<id_tipo>\d+)/$', 'cm.views.medicamentos_por_tipo', name='medicamentos_por_tipo'),
    url(r'^agregar/diagnostico/receta/$', 'cm.views.agregar_diagnostico', name='agregar_diagnostico'),
    url(r'^agregar/item/examen/$', 'cm.views.agregar_item', name='agregar_item'),
    url(r'^agregar/subitem/examen/$', 'cm.views.agregar_subitem', name='agregar_subitem'),
    url(r'^eliminar/tratamiento/$', 'cm.views.eliminar_tratamiento', name='eliminar_tratamiento'),
    url(r'^quitar/diagnostico/receta/$', 'cm.views.quitar_diagnostico_receta', name='quitar_diagnostico_receta'),


    # urls de recetas
    url(r'^administrador/receta/diagnostico/(?P<codigo>\d+)/$', 'cm.views.receta_diagnostico', name='receta_diagnostico'),
    url(r'^administrador/receta/tratamiento/(?P<codigo>\d+)/$', 'cm.views.receta_tratamiento', name='receta_tratamiento'),
    url(r'^administrador/receta/modificar/(?P<codigo>\d+)/$', 'cm.views.receta_modificar', name='receta_modificar'),
    url(r'^administrador/receta/modificar/(?P<id_receta>\d+)/tratamiento/(?P<id_tratamiento>\d+)$', 'cm.views.receta_modificar_tratamiento', name='receta_modificar_tratamiento'),
    url(r'^administrador/receta/modificar/(?P<id_receta>\d+)/diagnostico/(?P<id_diagnostico>\d+)$', 'cm.views.receta_modificar_diagnostico', name='receta_modificar_diagnostico'),
    url(r'^administrador/receta/imprimir/(?P<codigo>\d+)/$', 'cm.views.receta_imprimir', name='receta_imprimir'),


    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
