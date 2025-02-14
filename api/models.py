from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone



#maybe change this classname later?
class user(AbstractUser):
    email = models.EmailField(unique=True)
    date = models.DateTimeField(default=timezone.now);
    cpf = models.CharField(max_length=11);
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f"date: {self.date} | cpf {self.cpf}"