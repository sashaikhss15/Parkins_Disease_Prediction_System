from django.contrib.auth.models import User
from django.db import models


class PatientProfileModel(models.Model):
    # auth object
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100, error_messages={'required': 'Please Enter your name'}, default='')
    age = models.IntegerField(blank=True, default=0)
    gender = models.CharField(max_length=10, default='Male')
    smoker = models.CharField(max_length=10, default='No')
    height = models.CharField(max_length=20, default='0', help_text='5 ft. 6 in.')
    weight = models.IntegerField(error_messages={'required': 'Please Enter a numeric value'}, default=0, help_text='kg.')
    blood_pressure = models.IntegerField(error_messages={'required': 'Please Enter a numeric value'}, default=0)
    state = models.CharField(max_length=20, default='')
    city = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.user.username


class DoctorProfileModel(models.Model):
    # auth object
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100, error_messages={'required': 'Please Enter your name'}, default='Dr. ')
    age = models.IntegerField(blank=True, default=0)
    gender = models.CharField(max_length=10, default='Male')
    qualification = models.CharField(max_length=150, default='')
    clinic_address = models.TextField(max_length=300, default='', help_text='If Any', blank=True, null=True)
    state = models.CharField(max_length=20, default='')
    city = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.user.username

