from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    # Otros campos de la compañía

    def __str__(self):
        return self.nombre



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

