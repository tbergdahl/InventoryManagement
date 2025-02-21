from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class UType(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        EMPLOYEE = 'EMPLOYEE', 'Employee'
        NORMAL = 'NORMAL', 'Normal'
        
    usertype = models.CharField(max_length=10, choices= UType.choices, default=UType.NORMAL)