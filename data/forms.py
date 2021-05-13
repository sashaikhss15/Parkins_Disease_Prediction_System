from django import forms

from data.models import SymptomModel, DiseaseModel
from account.models import PatientProfileModel


class SymptomAddForm(forms.ModelForm):
    class Meta:
        model = SymptomModel
        fields = ['patient', 'voice_clip', 'symptom_description',]
        widgets = {
            'patient ': forms.ModelChoiceField(queryset=PatientProfileModel.objects.all()),
            'symptom_name': forms.TextInput(attrs={'class': 'form-control'}),
            'symptom_description': forms.Textarea(attrs={'class': 'form-control'}),
        }

        # def __str__(self):
        #     return self.Meta.model.symptom_name


class DiseaseAddForm(forms.ModelForm):
    class Meta:
        model = DiseaseModel
        fields = ['id','patient', 'fo', 'fhi', 'flo', 'jitter',
            'jitter_abs', 'rap', 'ppq', 'ddp', 'shimmer',
            'shimmer_db', 'shimmer_apq3', 'shimmer_apq5',
            'apq', 'dda', 'nhr', 'hnr', 'rpde', 'dfa',
            'spread1', 'spread2', 'd2', 'ppe',
        ]
        # widgets = {
        #     'disease_name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'disease_description': forms.Textarea(attrs={'class': 'form-control'}),
        # }

        # def __str__(self):
        #     return self.Meta.model.disease_name

class DiseaseEditForm(forms.ModelForm):
    class Meta:
        model = DiseaseModel
        fields = '__all__'
        # widgets = {
        #     'disease_name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'disease_description': forms.Textarea(attrs={'class': 'form-control'}),
        # }

        # def __str__(self):
        #     return self.Meta.model.disease_name
