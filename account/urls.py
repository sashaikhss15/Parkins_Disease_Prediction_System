from django.urls import path

from account import views

app_name = 'account'

urlpatterns = [
    path('', views.index, name='index'),
    path('register-patient/', views.register_patient, name='register_patient'),
    path('register-doctor/', views.register_doctor, name='register_doctor'),
    path('login-user/', views.login_user, name='login_user'),
    path('logout-user/', views.logout_user, name='logout_user'),
]
