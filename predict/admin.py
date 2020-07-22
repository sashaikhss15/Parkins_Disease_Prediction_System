from django.contrib import admin

from predict.models import PredictModel, PredictedDiseaseModel

admin.site.register(PredictModel)
admin.site.register(PredictedDiseaseModel)
