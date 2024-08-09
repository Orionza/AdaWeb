from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class MyUserManager(BaseUserManager):
    def create_user(self, Id_No, password=None, **extra_fields):
        if not Id_No:
            raise ValueError('The TC Kimlik No field must be set')
        extra_fields.setdefault('is_active', True)
        user = self.model(Id_No=Id_No, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, Id_No, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(Id_No, password, **extra_fields)

class MyUser(AbstractBaseUser, PermissionsMixin):
    Id_No = models.CharField(max_length=11, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()


    USERNAME_FIELD = 'Id_No'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']
    """
    def clean(self):
        super().clean()
        if len(self.Id_No) != 11:
            raise ValidationError(_('Id_No must be exactly 11 characters long.'))
    """
    def __str__(self):
        return self.Id_No

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    def save(self, *args, **kwargs):
        print("Saving user...")  # Bu mesajın göründüğünden emin ol
        super(MyUser, self).save(*args, **kwargs)
        print("User saved.")  # Eğer bu mesaj görünmezse, bir sorun var demektir
    




