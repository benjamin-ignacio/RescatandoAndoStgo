import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoRescatando.settings')
django.setup()

from mainApp.models import Usuario

# Mapeo de avatares antiguos a nuevos
mapeo_avatares = {
    'perro1': 'perro',
    'perro2': 'perro',
    'perro3': 'perro',
    'gato1': 'gato',
    'gato2': 'gato',
    'gato3': 'gato',
    'hamster': 'rata',
    'loro': 'pajaro',
    # conejo y tortuga se mantienen igual
}

print("=== Avatares actuales ===")
usuarios = Usuario.objects.all()
for usuario in usuarios:
    print(f"ID: {usuario.id}, Nombre: {usuario.nombre}, Avatar actual: {usuario.avatar}")

print("\n=== Actualizando avatares ===")
actualizados = 0
for usuario in usuarios:
    if usuario.avatar in mapeo_avatares:
        avatar_nuevo = mapeo_avatares[usuario.avatar]
        print(f"Cambiando {usuario.nombre}: {usuario.avatar} → {avatar_nuevo}")
        usuario.avatar = avatar_nuevo
        usuario.save()
        actualizados += 1
    else:
        print(f"Manteniendo {usuario.nombre}: {usuario.avatar}")

print(f"\n✅ Se actualizaron {actualizados} usuarios")

print("\n=== Avatares después de la actualización ===")
usuarios = Usuario.objects.all()
for usuario in usuarios:
    print(f"ID: {usuario.id}, Nombre: {usuario.nombre}, Avatar: {usuario.avatar}")
