import os
import sys
import django
from datetime import date

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoRescatando.settings')
django.setup()

from mainApp.models import Animal, FichaMedica, HogarTemporal, Voluntario, Usuario

print("=== SINCRONIZACIÓN DE ANIMALES CON BASE DE DATOS ===\n")

# 1. Obtener o crear hogar temporal
print("1. Verificando hogar temporal...")
try:
    admin = Usuario.objects.get(rol='admin')
    voluntario, created = Voluntario.objects.get_or_create(
        id_usuario=admin,
        defaults={'disponibilidad': 'Tiempo completo', 'experiencia': 'Más de 5 años'}
    )
    hogar, created = HogarTemporal.objects.get_or_create(
        id_voluntario=voluntario,
        defaults={'direccion': 'Refugio Central', 'espacio_disponible': 'Grande'}
    )
    print(f"✓ Hogar temporal: {hogar.direccion}\n")
except Exception as e:
    print(f"Error: {e}\n")
    sys.exit(1)

# 2. Crear animales con sus fichas médicas
print("2. Creando animales y fichas médicas...\n")

animales_data = [
    {
        'nombre': 'Akira',
        'especie': 'Gato',
        'edad': 2,
        'sexo': 'Hembra',
        'estado_salud': 'Excelente',
        'descripcion': 'Akira es un gato muy sano y activo.',
        'foto': 'animales/akira.jpg',
        'ficha': {
            'esterilizado': True,
            'fecha_esterilizacion': date(2024, 8, 15),
            'vacunas_al_dia': True,
            'ultima_vacunacion': '20/09/2024 (Triple Felina)',
            'ultimo_control': date(2024, 10, 5),
            'proximo_control': date(2025, 1, 5),
            'estado_salud': 'Excelente',
            'observaciones': 'Akira es un gato muy sano y activo. No presenta ninguna condición médica especial.'
        }
    },
    {
        'nombre': 'Rocky',
        'especie': 'Perro',
        'edad': 5,
        'sexo': 'Macho',
        'estado_salud': 'Bueno',
        'descripcion': 'Rocky es un perro amigable y juguetón.',
        'foto': 'animales/Rocky.jpg',
        'ficha': {
            'esterilizado': True,
            'fecha_esterilizacion': date(2023, 6, 10),
            'vacunas_al_dia': True,
            'ultima_vacunacion': '15/08/2024 (Antirrábica y Séxtuple)',
            'ultimo_control': date(2024, 9, 20),
            'proximo_control': date(2025, 2, 20),
            'estado_salud': 'Bueno',
            'observaciones': 'Rocky está en buenas condiciones. Requiere ejercicio regular.'
        }
    },
    {
        'nombre': 'Trufa',
        'especie': 'Gato',
        'edad': 3,
        'sexo': 'Hembra',
        'estado_salud': 'Excelente',
        'descripcion': 'Trufa es una gata cariñosa y tranquila.',
        'foto': 'animales/trufa.jpg',
        'ficha': {
            'esterilizado': True,
            'fecha_esterilizacion': date(2023, 11, 20),
            'vacunas_al_dia': True,
            'ultima_vacunacion': '10/09/2024 (Triple Felina)',
            'ultimo_control': date(2024, 10, 1),
            'proximo_control': date(2025, 1, 1),
            'estado_salud': 'Excelente',
            'observaciones': 'Trufa es una gata muy saludable. Perfecta para familias tranquilas.'
        }
    }
]

for data in animales_data:
    # Verificar si el animal ya existe
    animal = Animal.objects.filter(nombre=data['nombre']).first()
    
    if animal:
        print(f"⚠ {data['nombre']} ya existe en la base de datos")
        # Verificar si tiene ficha médica
        ficha = FichaMedica.objects.filter(id_animal=animal).first()
        if not ficha:
            ficha = FichaMedica.objects.create(id_animal=animal, **data['ficha'])
            print(f"✓ Ficha médica creada para {data['nombre']}")
        else:
            print(f"  Ficha médica ya existe")
    else:
        # Crear animal
        animal = Animal.objects.create(
            nombre=data['nombre'],
            especie=data['especie'],
            edad=data['edad'],
            sexo=data['sexo'],
            estado_salud=data['estado_salud'],
            descripcion=data['descripcion'],
            foto=data['foto'],
            disponible=True,
            id_hogar=hogar
        )
        print(f"✓ Animal creado: {data['nombre']}")
        
        # Crear ficha médica
        ficha = FichaMedica.objects.create(id_animal=animal, **data['ficha'])
        print(f"✓ Ficha médica creada para {data['nombre']}")
    
    print()

print("=== SINCRONIZACIÓN COMPLETADA ===")
print(f"Total animales en BD: {Animal.objects.count()}")
print(f"Total fichas médicas: {FichaMedica.objects.count()}")
