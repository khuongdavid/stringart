from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=30, unique=True)
    firstname = models.CharField(_('firs tname'), max_length=30)
    lastname = models.CharField(_('last name'), max_length=30)
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone'), max_length=11, default="", null= True)
    password = models.CharField(_('password'), max_length=255)
    image = models.ImageField(_('image'), upload_to='uploads/', null=True, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Contact(models.Model):
    firstname = models.CharField(_('first name'), max_length=30)
    lastname = models.CharField(_('last name'), max_length=30)
    email = models.EmailField(_('email address'), unique=False)
    message = models.TextField(_('message'), max_length=500)
    user = models.ForeignKey( User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.firstname + " " + self.lastname
