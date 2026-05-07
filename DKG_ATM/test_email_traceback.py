import os
import django
import sys
import traceback

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DKG_ATM.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("Sending test email to verify SMTP configuration...")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"EMAIL_HOST_PASSWORD length: {len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 0}")

try:
    send_mail(
        'DKG Bank - Test Email',
        'This is a test email to verify your SMTP configuration is working correctly.',
        settings.DEFAULT_FROM_EMAIL,
        [settings.EMAIL_HOST_USER], # Send to self
        fail_silently=False,
    )
    print("Email sent successfully! Please check your inbox.")
except Exception as e:
    print("Error sending email:")
    traceback.print_exc()
