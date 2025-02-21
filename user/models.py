from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email provided is incorrect.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say')
    )

    email = models.EmailField(unique=True, primary_key=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    first_name = models.CharField(max_length=255, blank=False, null=False)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    contact_number = models.CharField(max_length=13)
    
    USER_TYPE_CHOICES = (
        ('lawyer', 'Lawyer'),
        ('layman', 'Layman'),
        ('admin', 'Admin')
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
        
    def is_lawyer(self):
        return self.user_type == 'lawyer'

    def is_layman(self):
        return self.user_type == 'layman'
    
    def get_short_name(self) -> str:
        return self.email.split('@')[0]
    
    def get_profile(self):
        if self.is_lawyer():
            return getattr(self, "lawyer_profile")
        elif self.is_layman():
            return getattr(self, "layman_profile")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type', 'first_name', 'last_name', 'birth_date', 'gender']
    objects = CustomUserManager()

class Lawyer(CustomUser):
    roll_number = models.IntegerField(unique=True)
    roll_signed_date = models.DateField()

    ## PROFILE
    verified = models.BooleanField(default=False)
    cases_taken = models.IntegerField(default=0)

class Layman(CustomUser):
    pass