from django.contrib import admin

from predict.models import PredictModel, PredictedDiseaseModel, MyPredictModel

admin.site.register(PredictModel)
admin.site.register(PredictedDiseaseModel)
admin.site.register(MyPredictModel)