import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoRescatando.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("=== PROBANDO CONFIGURACIÓN DE EMAIL ===\n")
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD)}")
print("\nIntentando enviar email de prueba...\n")

try:
    send_mail(
        subject='Prueba de conexión - RescatandoAndo',
        message='Este es un email de prueba para verificar la configuración.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.EMAIL_HOST_USER],  # Enviar al mismo correo
        fail_silently=False,
    )
    print("✅ Email enviado correctamente!")
    print("La configuración está funcionando.")
except Exception as e:
    print(f"❌ Error al enviar email: {e}")
    print("\nPosibles soluciones:")
    print("1. Verifica que el correo rescatandoandostg@gmail.com existe")
    print("2. Verifica que la contraseña de aplicación 'dabj sidv bjon wtgv' es correcta")
    print("3. Si el correo es nuevo, intenta usar benjaminignacio1998@gmail.com")
    print("4. Verifica que tu firewall/antivirus no esté bloqueando el puerto 587")
