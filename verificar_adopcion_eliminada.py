import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoRescatando.settings')
django.setup()

from mainApp.models import Adopcion, SolicitudAdopcion, Adoptante

print("=== TODAS LAS ADOPCIONES ===")
adopciones = Adopcion.objects.all()
print(f"Total: {adopciones.count()}\n")
for a in adopciones:
    print(f"ID: {a.id}")
    print(f"Animal: {a.id_animal.nombre}")
    print(f"Adoptante: {a.id_adoptante.nombre}")
    print(f"Estado: {a.estado}")
    print(f"Fecha: {a.fecha_adopcion}")
    print("-" * 50)

print("\n=== SOLICITUDES APROBADAS ===")
solicitudes = SolicitudAdopcion.objects.filter(estado='aprobada')
print(f"Total: {solicitudes.count()}\n")
for s in solicitudes:
    print(f"ID: {s.id}")
    print(f"Animal: {s.id_animal.nombre}")
    print(f"Adoptante: {s.id_adoptante.nombre}")
    print(f"Estado: {s.estado}")
    # Verificar si tiene adopción asociada
    adopcion = Adopcion.objects.filter(solicitud_origen=s).first()
    if adopcion:
        print(f"✅ Tiene adopción asociada (ID: {adopcion.id})")
    else:
        print(f"❌ NO tiene adopción asociada")
    print("-" * 50)
