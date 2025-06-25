from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import *
from django.core.mail import send_mail
import random



#------------ ADMIN ----------------

def register_admin(request):
    error = None
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['pass']
        confirm_password = request.POST['con_pass']

        # Email format validation
        try:
            validate_email(email)
        except ValidationError:
            error = "Please enter a valid email address (e.g., name@example.com)."
            return render(request, 'register_admin.html', {'error': error})

        if password != confirm_password:
            error = "Passwords do not match."
        elif User.objects.filter(username=username).exists():
            error = "Username already exists."
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.is_staff = True
            user.save()
            adregister.objects.create(
                username=username,
                email=email,
                password=password,             
                confirm_password=confirm_password 
            )
            return redirect('login_admin')

    return render(request, 'register_admin.html', {'error': error})


def login_admin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass')
        try:
            user = adregister.objects.get(email=email, password=password)
            request.session['admin_id'] = user.id
            request.session['admin_email'] = user.email
            request.session['admin_name'] = user.username  # 👈 add this line
            return redirect('admin_dashboard') 
        except adregister.DoesNotExist:
            return render(request, 'login_admin.html', {'error': 'Invalid credentials'})

    return render(request, 'login_admin.html')


def logout_admin(request):
    request.session.flush()
    return redirect('login_admin')

    

def admin_dashboard(request):
    if 'admin_id' not in request.session: 
        return render(request, 'admin_dashboard.html')
    else:
        return render(request, 'admin_dashboard.html')

def forgot_password_admin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = adregister.objects.get(email=email)
            code = str(random.randint(100000, 999999))
            AdminOTP.objects.update_or_create(user=user, defaults={'code': code})
            send_mail(
                'Admin OTP Code',
                f'Your OTP is {code}',
                'pqr6997@gmail.com',
                [email]
            )
            return render(request, 'aenter_otp.html', {'email': email})
        except adregister.DoesNotExist:
            return render(request, 'admin_forgot.html', {'error': 'Admin user not found.'})

    return render(request, 'admin_forgot.html')


def verify_otp_admin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp_input = request.POST.get('otp')

        try:
            user = adregister.objects.get(email=email)

            try:
                otp_record = AdminOTP.objects.get(user=user)

                if otp_record.code == otp_input:
                    return render(request, 'reset_password_admin.html', {'email': email})
                else:
                    return render(request, 'aenter_otp.html', {
                        'email': email,
                        'error': 'Invalid OTP. Please try again.'
                    })

            except AdminOTP.DoesNotExist:
                return render(request, 'aenter_otp.html', {
                    'email': email,
                    'error': 'No OTP found for this admin.'
                })

        except adregister.DoesNotExist:
            return render(request, 'admin_forgot.html', {
                'error': 'Admin with this email does not exist.'
            })

    return redirect('forgot_password_admin')


def resend_otp_admin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = adregister.objects.get(email=email)
            new_code = str(random.randint(100000, 999999))
            AdminOTP.objects.update_or_create(user=user, defaults={'code': new_code})
            send_mail(
                'Admin OTP Code - Resend',
                f'Your new OTP is {new_code}',
                'pqr6997@gmail.com',
                [email]
            )
            return render(request, 'aenter_otp.html', {'email': email, 'message': 'OTP resent successfully!'})
        except adregister.DoesNotExist:
            return render(request, 'admin_forgot.html', {'error': 'Admin user not found.'})
    return redirect('forgot_password_admin')

        
def reset_password_admin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'reset_password_admin.html', {'email': email, 'error': 'Passwords do not match.'})

        try:
            user = adregister.objects.get(email=email)
            user.password = password
            user.confirm_password = confirm_password
            user.save()
            AdminOTP.objects.filter(user=user).delete()
            return redirect('login_admin')  # your admin login URL name
        except adregister.DoesNotExist:
            return render(request, 'reset_password_admin.html', {'email': email, 'error': 'User not found.'})

    return redirect('forgot_password_admin')


# ---------- DISTRIBUTOR ----------

def register_distributor(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('Username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_pass')

        # Email format check
        try:
            validate_email(email)
        except ValidationError:
            error = "Please enter a valid email address (e.g., name@example.com)."
            return render(request, 'register_distributor.html', {'error': error})

        if password != confirm_password:
            error = "Passwords do not match."
        elif User.objects.filter(username=username).exists():
            error = "Username already exists."
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.is_staff = False 
            user.save()

            register.objects.create(
                username=username,
                email=email,
                password=password,             
                confirm_password=confirm_password 
            )

            return redirect('login_distributor')

    return render(request, 'register_distributor.html', {'error': error})



def login_distributor(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = register.objects.get(email=email, password=password)
            request.session['distributor_id'] = user.id
            request.session['distributor_email'] = user.email
            request.session['distributor_username'] = user.username 
            return redirect('distributor_dashboard')
        except register.DoesNotExist:
            return render(request, 'login_distributor.html', {'error': 'Invalid credentials'})

    return render(request, 'login_distributor.html')


def logout_distributor(request):
    request.session.flush()
    return redirect('login_distributor')




def distributor_dashboard(request):
    if 'distributor_id' not in request.session: 
      return render(request, 'distributor_dashboard.html')
    else:
      return render(request, 'distributor_dashboard.html')
        

def forgot_password_distributor(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = register.objects.get(email=email)  # ✅ custom register model
            code = str(random.randint(100000, 999999))
            
            # ✅ create or update OTP for this custom user
            OTP.objects.update_or_create(user=user, defaults={'code': code})
            
            send_mail(
                'Distributor OTP Code',
                f'Your OTP is {code}',
                'pqr6997@gmail.com',
                [email]
            )
            return render(request, 'denter_otp.html', {'email': email})
        except register.DoesNotExist:  # ✅ must match your model
            return render(request, 'distributor_forgot.html', {'error': 'Distributor not found'})
    return render(request, 'distributor_forgot.html')


def verify_otp_distributor(request):
    if request.method == 'POST':
        email = request.POST['email']
        otp = request.POST['otp']

        try:
            user = register.objects.get(email=email)

            try:
                record = OTP.objects.get(user=user)

                if record.code == otp:
                    return render(request, 'reset_password_distributor.html', {'email': email})
                else:
                    return render(request, 'denter_otp.html', {
                        'email': email,
                        'error': 'Invalid OTP. Please try again.'
                    })

            except OTP.DoesNotExist:
                return render(request, 'denter_otp.html', {
                    'email': email,
                    'error': 'No OTP found for this user.'
                })

        except register.DoesNotExist:
            return render(request, 'distributor_forgot.html', {
                'error': 'Email does not exist in system.'
            })

    return redirect('forgot_password_distributor')


def resend_otp_distributor(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = register.objects.get(email=email)
            new_code = str(random.randint(100000, 999999))
            OTP.objects.update_or_create(user=user, defaults={'code': new_code})
            send_mail(
                'Distributor OTP Code - Resend',
                f'Your new OTP is {new_code}',
                'pqr6997@gmail.com',
                [email]
            )
            return render(request, 'denter_otp.html', {'email': email, 'message': 'OTP resent successfully!'})
        except register.DoesNotExist:
            return render(request, 'distributor_forgot.html', {'error': 'Distributor not found.'})
    return redirect('forgot_password_distributor')

def reset_password_distributor(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not email:
            return render(request, 'reset_password_distributor.html', {'error': 'Email is missing.'})

        if new_password != confirm_password:
            return render(request, 'reset_password_distributor.html', {
                'email': email,
                'error': 'Passwords do not match.'
            })

        try:
            user = register.objects.get(email=email)  # fetch by email

            user.password = new_password
            user.confirm_password = confirm_password
            user.save()

            # Delete OTP after successful reset
            OTP.objects.filter(user=user).delete()

            return redirect('login_distributor')

        except register.DoesNotExist:
            return render(request, 'reset_password_distributor.html', {
                'email': email,
                'error': 'User not found.'
            })

    return redirect('forgot_password_distributor')

