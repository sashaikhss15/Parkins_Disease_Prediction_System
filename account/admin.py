from django.contrib import admin

from account.models import PatientProfileModel, DoctorProfileModel

admin.site.register(PatientProfileModel)
admin.site.register(DoctorProfileModel)
