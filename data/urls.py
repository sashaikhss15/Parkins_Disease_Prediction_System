"""DPS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views

app_name = 'data'

urlpatterns = [
    path('', views.index, name="index"),
    # SYMPTOMS
    # /data/symptoms-list/
    path('symptoms-list/', views.symptoms_list, name="symptoms-list"),
    # /data/symptom-add/
    path('symptom-add/', views.symptom_add, name="symptom-add"),
    # /data/symptom-detail/12/delete
    path('symptom-detail/<int:symptom_id>/delete/', views.symptom_delete, name="symptom-delete"),
    # /data/symptom-detail/12/
    path('symptom-detail/<int:symptom_id>/', views.symptom_detail, name="symptom-details"),

    # DISEASES
    # /data/diseases-list/
    path('diseases-list/', views.diseases_list, name="diseases-list"),
    # /data/disease-add/
    path('disease-add/', views.disease_add, name="disease-add"),
    # /data/disease-detail/12/delete
    path('disease-detail/<int:disease_id>/delete/', views.disease_delete, name="disease-delete"),
    # /data/disease-detail/12/
    path('disease-detail/<int:disease_id>/', views.disease_detail, name="disease-details"),
    # /data/disease-edit/11/
    path('disease-edit/<int:disease_id>/', views.disease_edit, name="disease-edit"),

    path('disease-get/', views.disease_get, name='disease-get'),

    path('disease-update/<int:instance_id>/', views.disease_update, name='disease-update')

]
