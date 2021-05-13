from django.contrib import admin

# Register your models here.
from data.models import SymptomModel, DiseaseModel

admin.site.register(SymptomModel)
admin.site.register(DiseaseModel)
