from django.db import models
from account.models import PatientProfileModel


# Create your models here.
class SymptomModel(models.Model):
    symptom_name = models.CharField(max_length=100)
    description = models.TextField()
    patient = models.ForeignKey(PatientProfileModel, on_delete=models.CASCADE, null=True, blank=True)
    voice_clip = models.FileField(upload_to='voice_clips/', null=True, blank=True)

    def __str__(self):
        return self.patient.name


class DiseaseModel(models.Model):
    # remove this field
    # disease_name = models.CharField(max_length=100)
    # disease_description = models.TextField()
    # Add fields 
    patient = models.ForeignKey(PatientProfileModel, on_delete=models.CASCADE, null=True, blank=True)
    fo = models.FloatField(null=True, blank=True)
    fhi = models.FloatField(null=True, blank=True)
    flo = models.FloatField(null=True, blank=True)
    jitter = models.FloatField(null=True, blank=True)
    jitter_abs = models.FloatField(null=True, blank=True)
    rap = models.FloatField(null=True, blank=True)
    ppq = models.FloatField(null=True, blank=True)
    ddp = models.FloatField(null=True, blank=True)
    shimmer = models.FloatField(null=True, blank=True)
    shimmer_db = models.FloatField(null=True, blank=True)
    shimmer_apq3 = models.FloatField(null=True, blank=True)
    shimmer_apq5 = models.FloatField(null=True, blank=True)
    apq = models.FloatField(null=True, blank=True)
    dda = models.FloatField(null=True, blank=True)
    nhr = models.FloatField(null=True, blank=True)
    hnr = models.FloatField(null=True, blank=True)
    rpde = models.FloatField(null=True, blank=True)
    dfa = models.FloatField(null=True, blank=True)
    spread1 = models.FloatField(null=True, blank=True)
    spread2 = models.FloatField(null=True, blank=True)
    d2 = models.FloatField(null=True, blank=True)
    ppe = models.FloatField(null=True, blank=True)
    parameters_file = models.FileField(upload_to='parameters_files/', null=True, blank=True)

    def __str__(self):
        return self.patient.name