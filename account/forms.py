from django import forms
from django.contrib.auth.models import User

from account.models import PatientProfileModel, DoctorProfileModel


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']
        help_texts = {
            'username': 'used for login',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        if 'password' in self.cleaned_data and 'confirm_password' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
                print('--------------raising validation erro')
                raise forms.ValidationError('Password Mismatched')

        if 'username' in self.cleaned_data:
            try:
                user = User.objects.get(username=self.cleaned_data['username'])
                raise forms.ValidationError('Username already taken')
            except User.DoesNotExist:
                pass

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class PatientProfileForm(forms.ModelForm):
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    smoker_choices = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    gender = forms.ChoiceField(choices=gender_choices, required=False,
                               widget=forms.Select(
                                   attrs={'class': 'form-inline form-control btn btn-default dropdown-toggle'}))
    smoker = forms.ChoiceField(choices=smoker_choices, required=False,
                               widget=forms.Select(
                                   attrs={'class': 'form-inline form-control btn btn-default dropdown-toggle'}))

    class Meta:
        model = PatientProfileModel
        fields = ['name', 'gender', 'smoker', 'height', 'age', 'weight', 'blood_pressure', 'state', 'city']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'height': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'blood_pressure': forms.NumberInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PatientEditProfileForm(forms.ModelForm):
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    smoker_choices = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    gender = forms.ChoiceField(choices=gender_choices, required=False,
                               widget=forms.Select(
                                   attrs={'class': 'form-inline form-control btn btn-default dropdown-toggle'}))
    smoker = forms.ChoiceField(choices=smoker_choices, required=False,
                               widget=forms.Select(
                                   attrs={'class': 'form-inline form-control btn btn-default dropdown-toggle'}))

    class Meta:
        model = PatientProfileModel
        fields = ['name', 'gender', 'smoker', 'height', 'age', 'weight', 'blood_pressure', 'state', 'city']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'readonly': ''}),
            'height': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'blood_pressure': forms.NumberInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }


class DoctorProfileForm(forms.ModelForm):
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    gender = forms.ChoiceField(choices=gender_choices, required=False,
                               widget=forms.Select(
                                   attrs={'class': 'form-inline form-control btn btn-default dropdown-toggle'}))

    class Meta:
        model = DoctorProfileModel
        fields = ['name', 'qualification', 'gender', 'age', 'clinic_address', 'state', 'city']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'clinic_address': forms.Textarea(attrs={'class': "form-control", '!required': '',
                                                    'rows': '3'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }


class DoctorEditProfileForm(forms.ModelForm):
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    gender = forms.ChoiceField(choices=gender_choices, required=False,
                               widget=forms.Select(
                                   attrs={'class': 'form-inline form-control btn btn-default dropdown-toggle'}))

    class Meta:
        model = DoctorProfileModel
        fields = ['name', 'qualification', 'gender', 'age', 'clinic_address', 'state', 'city']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'readonly': ''}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'clinic_address': forms.Textarea(attrs={'class': "form-control", '!required': '',
                                                    'rows': '3'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }
