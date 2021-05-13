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

app_name = 'predict'

urlpatterns = [
    path('parkinson-predict/', views.parkinson_predict, name="parkinson_predict"),
    path('post-parameter-in-model/', views.post_parameter_in_model, name="post_parameter_in_model"),
    path('', views.index, name="index"),
    path('history/', views.history, name="history"),
    path('<int:predict_model_id>/result/', views.result, name="result"),
    path('approvals/', views.approvals, name="approvals"),
    path('approvals/<int:approval_id>/approve/', views.approve, name="approve"),
    path('approvals/<int:reject_id>/reject/', views.reject, name="reject"),
]
