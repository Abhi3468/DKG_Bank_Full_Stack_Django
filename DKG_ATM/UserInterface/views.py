from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from BankInterface.models import Account
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import json
import random
import string
from django import forms

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

def generate_card_number():
    return ''.join(random.choices(string.digits, k=16))

def generate_pin():
    return ''.join(random.choices(string.digits, k=4))
def index(request):
    if request.user.is_authenticated:
        return render(request, "next_page.html")
    return render(request, "index.html")

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = None
            try:
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password']
                )
            except Exception as e:
                import traceback
                print(f"[REGISTER ERROR] Failed to create user: {e}", flush=True)
                traceback.print_exc()
                return JsonResponse({
                    'success': False,
                    'message': f'Failed to create user account: {str(e)}'
                }, status=500)

            # Create associated account
            try:
                card_number = generate_card_number()
                pin = generate_pin()
                account = Account.objects.create(
                    user=user,
                    card_number=card_number,
                    card_pin=pin,
                    balance=1000.00
                )
            except Exception as e:
                import traceback
                print(f"[REGISTER ERROR] Failed to create bank account: {e}", flush=True)
                traceback.print_exc()
                # Clean up the user since account creation failed
                if user:
                    try:
                        user.delete()
                    except Exception:
                        pass
                return JsonResponse({
                    'success': False,
                    'message': f'Failed to create bank account: {str(e)}'
                }, status=500)
            
            # Fetch generated details
            customer_name = user.username
            customer_id = account.customer_id
            account_number = account.account_number
            ifsc_code = account.ifsc_code
            
            # Prepare email
            subject = 'DKG Bank - Your Account Registration Details'
            message = (
                f"Welcome to DKG Bank, {customer_name}!\n\n"
                f"Your account has been successfully created. Here are your account and card details:\n\n"
                f"--------------------------------------\n"
                f"Customer Name:  {customer_name}\n"
                f"Customer ID:    {customer_id}\n"
                f"Account Number: {account_number}\n"
                f"IFSC Code:      {ifsc_code}\n\n"
                f"ATM Card Number: {card_number}\n"
                f"ATM PIN:        {pin}\n"
                f"--------------------------------------\n\n"
                f"⚠️ SECURITY ALERT:\n"
                f"Please store these details securely. NEVER share your card details, PIN, or password with anyone, including bank employees.\n\n"
                f"Thank you for banking with us,\n"
                f"DKG Bank Team"
            )
            
            # Send Email (non-blocking — registration succeeds even if email fails)
            email_sent = False
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                email_sent = True
                print(f"\n[BANK SECURITY] Registration details sent via email to {user.email}\n", flush=True)
            except Exception as mail_err:
                print(f"[REGISTER WARNING] Mail Error during registration: {mail_err}", flush=True)
            
            try:
                login(request, user)
            except Exception as login_err:
                print(f"[REGISTER WARNING] Auto-login failed: {login_err}", flush=True)

            return JsonResponse({
                'success': True, 
                'message': 'Account created successfully!',
                'email_sent': email_sent,
                'card_number': card_number,
                'card_pin': pin,
                'customer_id': customer_id,
                'account_number': account_number,
                'ifsc_code': ifsc_code
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors.as_json()}, status=400)
    return render(request, "register.html")

def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        method = data.get('method', 'password')
        
        if method == 'password':
            password = data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True}, status=200)
            else:
                return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=401)
        elif method == 'otp':
            otp_input = data.get('otp')
            session_otp = request.session.get('login_otp')
            session_username = request.session.get('login_otp_username')
            
            if otp_input and session_otp and str(otp_input) == str(session_otp) and username == session_username:
                user = User.objects.get(username=username)
                login(request, user)
                # Clear session
                if 'login_otp' in request.session: del request.session['login_otp']
                if 'login_otp_username' in request.session: del request.session['login_otp_username']
                return JsonResponse({'success': True}, status=200)
            else:
                return JsonResponse({'success': False, 'message': 'Invalid OTP'}, status=401)
    return render(request, "index.html")

def send_login_otp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            
            if not username:
                return JsonResponse({'success': False, 'message': 'Username is required.'}, status=400)
            
            user_obj = User.objects.filter(username=username).first()
            if not user_obj:
                return JsonResponse({'success': False, 'message': 'User not found.'}, status=404)
                
            if not user_obj.email:
                return JsonResponse({'success': False, 'message': 'No email associated with this account. Please contact support.'}, status=400)
                
            otp = ''.join(random.choices(string.digits, k=6))
            request.session['login_otp'] = otp
            request.session['login_otp_username'] = username
            
            # Send Email
            subject = 'DKG Bank - Your Login OTP'
            message = f'Hello {username},\n\nYour One-Time Password (OTP) for login is: {otp}\n\nThis OTP is valid for a short time. Do not share this with anyone.\n\nThank you,\nDKG Bank Security'
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user_obj.email],
                    fail_silently=False,
                )
                print(f"\n[BANK SECURITY] Login OTP sent via email to {user_obj.email}: {otp}\n", flush=True)
                return JsonResponse({'success': True, 'message': 'OTP sent to your registered email successfully!'}, status=200)
            except Exception as mail_err:
                print(f"Mail Error: {mail_err}")
                return JsonResponse({'success': False, 'message': 'Failed to send email. Please check SMTP settings.'}, status=500)
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid request.'}, status=405)

def logout_view(request):
    logout(request)
    return redirect('index')

def next_page(request):
    if not request.user.is_authenticated:
        return redirect('index')
    return render(request, "next_page.html")
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if not user:
            return JsonResponse({'success': False, 'message': 'No account found with this email.'})
            
        try:
            otp = ''.join(random.choices(string.digits, k=6))
            request.session['reset_otp'] = otp
            request.session['reset_user_id'] = user.id
            
            # Send Email
            subject = 'DKG Bank - Password Reset OTP'
            message = f'Hello {user.username},\n\nYour One-Time Password (OTP) for resetting your password is: {otp}\n\nThis OTP is valid for a short time. Do not share this with anyone.\n\nIf you did not request a password reset, please ignore this email.\n\nThank you,\nDKG Bank Security'
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            print(f"\n[BANK SECURITY] Password reset OTP sent via email to {user.email}: {otp}\n", flush=True)
            return JsonResponse({'success': True, 'message': 'OTP sent to your email.'})
        except Exception as mail_err:
            print(f"Mail Error: {mail_err}")
            return JsonResponse({'success': False, 'message': 'Failed to send email. Please check SMTP settings.'}, status=500)
    return render(request, "forgot_password.html")

def verify_otp(request):
    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        if otp_input == request.session.get('reset_otp'):
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'message': 'Invalid OTP.'})
    return render(request, "verify_otp.html")

def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('password')
        user_id = request.session.get('reset_user_id')
        if user_id:
            user = User.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()
            # Clean up session
            del request.session['reset_otp']
            del request.session['reset_user_id']
            return JsonResponse({'success': True, 'message': 'Password reset successful!'})
        return JsonResponse({'success': False, 'message': 'Session expired.'})
    return render(request, "reset_password.html")

def db_health(request):
    """
    A diagnostic endpoint to check the database and environment configuration.
    Visit /db-health/ on your Render site to see the status.
    Only accessible in DEBUG mode OR with a secret key param for safety.
    """
    import os
    from django.db import connection
    from django.conf import settings
    
    # Basic security: only allow in DEBUG mode or if secret param matches
    secret = request.GET.get('key', '')
    allowed = settings.DEBUG or secret == os.environ.get('HEALTH_CHECK_KEY', '')
    if not allowed:
        return JsonResponse({'error': 'Not authorized. Set HEALTH_CHECK_KEY env var and pass ?key=... to access.'}, status=403)

    result = {
        'status': 'checking',
        'database': {},
        'environment': {},
        'tables': [],
        'errors': [],
    }

    # Check environment vars
    result['environment'] = {
        'DEBUG': str(settings.DEBUG),
        'DATABASE_URL_SET': bool(os.environ.get('DATABASE_URL')),
        'DATABASE_ENGINE': settings.DATABASES['default'].get('ENGINE', 'unknown'),
        'DATABASE_HOST': settings.DATABASES['default'].get('HOST', 'N/A'),
        'DATABASE_NAME': settings.DATABASES['default'].get('NAME', 'N/A'),
        'EMAIL_HOST_USER_SET': bool(getattr(settings, 'EMAIL_HOST_USER', None)),
        'EMAIL_HOST_PASSWORD_SET': bool(getattr(settings, 'EMAIL_HOST_PASSWORD', None)),
    }

    # Try DB connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        result['database']['connection'] = 'OK'
        
        # List all tables
        try:
            with connection.cursor() as cursor:
                if 'sqlite' in settings.DATABASES['default'].get('ENGINE', ''):
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
                else:
                    cursor.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname='public' ORDER BY tablename;")
                tables = [row[0] for row in cursor.fetchall()]
                result['tables'] = tables

            # Check critical tables
            critical_tables = ['auth_user', 'BankInterface_account', 'django_session', 'django_migrations']
            missing = [t for t in critical_tables if t not in tables]
            result['database']['critical_tables_present'] = [t for t in critical_tables if t in tables]
            result['database']['critical_tables_missing'] = missing
            
            if missing:
                result['status'] = 'ERROR - missing tables (run migrations)'
                result['errors'].append(f"Missing tables: {missing}. Run: python manage.py migrate")
            else:
                result['status'] = 'OK'
        except Exception as te:
            result['database']['tables_error'] = str(te)
            result['status'] = 'partial'

    except Exception as e:
        result['database']['connection'] = 'FAILED'
        result['database']['error'] = str(e)
        result['status'] = 'ERROR - cannot connect to database'
        result['errors'].append(str(e))

    return JsonResponse(result, json_dumps_params={'indent': 2})

