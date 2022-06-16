from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import AbstractUser, BaseUserManager



# Create your models here.
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = ((GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female'))
    ROLES = (

        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patients', 'Patients'),

    )


    role = models.CharField(max_length=15 ,default="none",null=True ,blank=True)
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    clinic_name = models.CharField(max_length=30,default=None,blank=True,null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES,default=None,null=True,blank=True)
    specialty = models.CharField(max_length=30,default=None,blank=True,null=True)
    address = models.TextField(default=None,blank=True,null=True)
    profile = models.FileField(upload_to='user',default='profile.png')
   
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return  self.name +" "+ self.email

class UserToken(models.Model):
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    token = models.CharField(null=True, max_length=500)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return str(self.user)


class Doctor_availability(models.Model):
    WEEKS = {
        (1,'MONDAY'),
        (2,'TUESDAY'),
        (3,'WEDNESDAY'),
        (4,'THURSDAY'),
        (5,'FRIDAY'),
        (6,'SATURDAY'),
    }
    doctor = models.ForeignKey(User,on_delete=models.CASCADE)
    week = models.IntegerField(choices=WEEKS)
    start_time = models.TimeField('start time')
    end_time = models.TimeField('end time')

    def __int__(self):
        return self.week



class Appoinment(models.Model):
    STATUS = (
        (0,'Pending'),
        (1,'Completed'),
        (2,'Absent'),
        (3,'Canceled'),
    ) 
    doctor = models.ForeignKey(User,related_name='doctor_aap' ,on_delete=models.CASCADE)
    patient = models.ForeignKey(User,related_name='patient_app',on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField('start time')
    end_time = models.TimeField('end time')
    description = models.TextField( default=None)
    status = models.IntegerField(default=0,choices=STATUS)


    def __int__(self):
        return self.doctor.name

    def __str__(self):
        return self.patient.name