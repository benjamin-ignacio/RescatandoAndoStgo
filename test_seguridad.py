import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoRescatando.settings')
django.setup()

from mainApp.models import Usuario
from django.contrib.auth.hashers import make_password

print("=== PRUEBAS DE SEGURIDAD ===\n")

# 1. Prueba de inyección SQL
print("1. PRUEBA DE INYECCIÓN SQL")
intentos_sql = [
    "' OR '1'='1",
    "admin' --",
    "' OR 1=1 --",
    "admin'/*",
    "' UNION SELECT NULL--",
]

for intento in intentos_sql:
    try:
        resultado = Usuario.objects.filter(cuenta=intento)
        if resultado.exists():
            print(f"   ⚠️ VULNERABLE: '{intento}' retornó usuarios")
        else:
            print(f"   ✅ SEGURO: '{intento}' no retornó usuarios")
    except Exception as e:
        print(f"   ✅ PROTEGIDO: '{intento}' causó excepción (esperado)")

# 2. Prueba de XSS en nombres
print("\n2. PRUEBA DE XSS EN NOMBRES")
scripts_xss = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror='alert(1)'>",
    "javascript:alert('XSS')",
    "<svg onload=alert('XSS')>",
]

print("   Intentando crear usuarios con código malicioso...")
for script in scripts_xss:
    try:
        usuario = Usuario.objects.create(
            nombre=script,
            cuenta=f"test_{script[:10]}",
            email="test@test.com",
            contraseña=make_password("test123"),
            rol='usuario'
        )
        # Verificar si se escapó correctamente
        if "<" in usuario.nombre or ">" in usuario.nombre:
            print(f"   ⚠️ VULNERABLE: Script guardado sin escapar")
        else:
            print(f"   ✅ SEGURO: Script fue sanitizado")
        usuario.delete()
    except Exception as e:
        print(f"   ✅ PROTEGIDO: Excepción al intentar guardar script")

# 3. Prueba de límites de longitud
print("\n3. PRUEBA DE LÍMITES DE LONGITUD")
texto_largo = "A" * 10000
try:
    usuario = Usuario.objects.create(
        nombre=texto_largo,
        cuenta="test_largo",
        email="largo@test.com",
        contraseña=make_password("test123"),
        rol='usuario'
    )
    print(f"   ⚠️ VULNERABLE: Aceptó texto de {len(texto_largo)} caracteres")
    usuario.delete()
except Exception as e:
    print(f"   ✅ PROTEGIDO: Rechazó texto excesivamente largo ({type(e).__name__})")

# 4. Prueba de emails inválidos
print("\n4. PRUEBA DE VALIDACIÓN DE EMAIL")
emails_invalidos = [
    "correo@",
    "@gmail.com",
    "correo sin arroba",
    "correo@dominio",
    "correo@@dominio.com",
]

from mainApp.views import validate_email
for email in emails_invalidos:
    resultado = validate_email(email)
    if resultado:
        print(f"   ⚠️ VULNERABLE: '{email}' fue aceptado")
    else:
        print(f"   ✅ SEGURO: '{email}' fue rechazado")

# 5. Verificar sanitización
print("\n5. PRUEBA DE SANITIZACIÓN")
from mainApp.views import sanitize_input
textos_peligrosos = [
    "<script>alert('XSS')</script>",
    "Normal text with <b>HTML</b>",
    "'; DROP TABLE usuarios; --",
]

for texto in textos_peligrosos:
    sanitizado = sanitize_input(texto)
    if "<" in sanitizado or ">" in sanitizado:
        print(f"   ⚠️ VULNERABLE: HTML no escapado en '{texto[:30]}'")
    else:
        print(f"   ✅ SEGURO: '{texto[:30]}' fue sanitizado correctamente")

print("\n=== FIN DE PRUEBAS ===")
