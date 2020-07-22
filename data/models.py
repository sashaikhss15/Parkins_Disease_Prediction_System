from django.db import models


# Create your models here.
class SymptomModel(models.Model):
    symptom_name = models.CharField(max_length=100)
    symptom_description = models.TextField()

    def __str__(self):
        return self.symptom_name


class DiseaseModel(models.Model):
    disease_name = models.CharField(max_length=100)
    disease_description = models.TextField()

    def __str__(self):
        return self.disease_name
