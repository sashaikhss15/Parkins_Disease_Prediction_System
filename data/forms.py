from django import forms

from data.models import SymptomModel, DiseaseModel
from account.models import PatientProfileModel

from upload_validator import FileTypeValidator

class SymptomAddForm(forms.ModelForm):
    class Meta:
        model = SymptomModel
        fields = ['patient', 'voice_clip', 'description',]
        widgets = {
            'patient ': forms.ModelChoiceField(queryset=PatientProfileModel.objects.all()),
            'symptom_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            # 'voice_clip' : forms.FileField(
            #                 label='', help_text="Only image formats are accepted.", required=False,
                            
            #                 )
            # 'voice_clip': forms.FileField(attrs={'class': 'form-control'}),
        }

        # def __str__(self):
        #     return self.Meta.model.symptom_name


class DiseaseAddForm(forms.ModelForm):
    class Meta:
        model = DiseaseModel
        fields = ['id','patient', 'parameters_file', 'fo', 'fhi', 'flo', 'jitter',
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
