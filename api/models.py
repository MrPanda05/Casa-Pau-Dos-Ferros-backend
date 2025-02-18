from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    full_name = models.CharField(max_length=150, unique=False, default='User');
    birth_date = models.DateField(default=timezone.now);
    cpf = models.CharField(max_length=11, null=False, default='00000000000');
    
    def __str__(self):
        return self.username

class user_address(models.Model):
    address_id = models.AutoField(primary_key=True)
    cep = models.CharField(max_length=8, null=False)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=80)
    number = models.CharField(max_length=8)
    complement = models.CharField(max_length=80, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(User, models.CASCADE, db_column='user_id', null=True, default=0)

    def __str__(self):
        return self.address_id