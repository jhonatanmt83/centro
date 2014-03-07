#encoding:utf-8
from cm.models import Paquete


def ObtenerPaquetes():
    paquetes_total = Paquete.objects.all()
    seleccionado = []
    for paquete in paquetes_total:
        seleccionado.append((str(paquete.pk), paquete.nombre))
    seleccionado = tuple(seleccionado)
    return seleccionado