from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *
urlpatterns = [
    path('register/admin/',register_admin, name='register_admin'),
    path('login/admin/', login_admin, name='login_admin'),
    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),
    path('forgot-password/admin/', forgot_password_admin, name='forgot_password_admin'),
    path('verify-otp/admin/', verify_otp_admin, name='verify_otp_admin'),
    path('reset-password/admin/', reset_password_admin, name='reset_password_admin'),
    path('resend-otp/admin/', resend_otp_admin, name='resend_otp_admin'),
    path('logout_admin/admin',logout_admin,name='logout_admin'),


    path('register/distributor/', register_distributor, name='register_distributor'),
    path('login/distributor/', login_distributor, name='login_distributor'),
    path('', distributor_dashboard, name='distributor_dashboard'),
    path('forgot-password/distributor/', forgot_password_distributor, name='forgot_password_distributor'),
    path('verify-otp/distributor/', verify_otp_distributor, name='verify_otp_distributor'),
    path('reset-password/distributor/', reset_password_distributor, name='reset_password_distributor'),
    path('resend-otp/distributor/', resend_otp_distributor, name='resend_otp_distributor'),
    path('logout_distributor/distributor',logout_distributor,name='logout_distributor'),
    


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)