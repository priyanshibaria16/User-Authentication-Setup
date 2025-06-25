from django.db import models
from django.contrib.auth.models import User




    
class register(models.Model):
    username=models.CharField(max_length=50)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=50)
    confirm_password=models.CharField(max_length=50)
 

    def __str__(self):
        return self.username
        
class adregister(models.Model):
    username=models.CharField(max_length=50)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=50)
    confirm_password=models.CharField(max_length=50)
   

    def __str__(self):
        return self.username
    
class OTP(models.Model):
    user = models.ForeignKey(register, on_delete=models.CASCADE)  # Link to distributor only
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.code}"
    
class AdminOTP(models.Model):
    user = models.ForeignKey(adregister, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.code}"
