from django import forms

from .models import PredictModel, PredictedDiseaseModel


class PredictForm(forms.ModelForm):
    class Meta:
        model = PredictModel
        fields = ['patient_name', 'patient_username', 'symptoms']
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'form-control', 'readonly': ''}),
            'patient_username': forms.TextInput(attrs={'class': 'form-control', 'readonly': ''}),
        }
        error_messages = {
            'symptoms': {
                'required': 'Please select at-least one symptom'
            },
        }


class PredictedDiseaseForm(forms.ModelForm):
    class Meta:
        model = PredictedDiseaseModel
        fields = '__all__'
        widgets = {
            'approved_by': forms.TextInput(attrs={'!required': '', }),
            'rejected_by': forms.TextInput(attrs={'!required': '', })
        }
