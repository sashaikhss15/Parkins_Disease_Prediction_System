from django.urls import path

from account import views

app_name = 'account'

urlpatterns = [
    path('', views.index, name='index'),
    path('doctor-account', views.doctor_account_index, name='doctor_account_index'),
    path('register-patient/', views.register_patient, name='register_patient'),
    path('patient-list/', views.patient_list, name='patient_list'),
    path('patient-detail/<int:patient_id>/', views.patient_detail, name="patient_details"),
    path('patient-detail/<int:patient_id>/delete/', views.patient_delete, name="patient_delete"),
    path('patient-edit/<int:patient_id>/', views.patient_edit, name="patient_edit"),
    path('register-doctor/', views.register_doctor, name='register_doctor'),
    path('login-user/', views.login_user, name='login_user'),
    path('logout-user/', views.logout_user, name='logout_user'),
]
