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
    url(r'^administrador/caja$', 'cm.views.egresos', name='caja'),
    url(r'^administrador/examen/(?P<codigo>\d+)/$', 'cm.views.examen', name='examen'),

    url(r'^precio/paquete/(?P<codigo>\d+)/$', 'cm.views.precio_paquete', name='precio_paquete'),


    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
