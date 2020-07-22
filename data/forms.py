from django import forms

from data.models import SymptomModel, DiseaseModel


class SymptomAddForm(forms.ModelForm):
    class Meta:
        model = SymptomModel
        fields = '__all__'
        widgets = {
            'symptom_name': forms.TextInput(attrs={'class': 'form-control'}),
            'symptom_description': forms.Textarea(attrs={'class': 'form-control'}),
        }

        # def __str__(self):
        #     return self.Meta.model.symptom_name


class DiseaseAddForm(forms.ModelForm):
    class Meta:
        model = DiseaseModel
        fields = '__all__'
        widgets = {
            'disease_name': forms.TextInput(attrs={'class': 'form-control'}),
            'disease_description': forms.Textarea(attrs={'class': 'form-control'}),
        }

        # def __str__(self):
        #     return self.Meta.model.disease_name
