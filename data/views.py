import os
import pandas as pd

from django.shortcuts import render, get_object_or_404, redirect

from .forms import SymptomAddForm, DiseaseAddForm, DiseaseEditForm
from .models import SymptomModel, DiseaseModel


# Create your views here.


def index(request):
    return render(request, 'data/index.html')


def symptoms_list(request):
    symptoms = SymptomModel.objects.all()
    return render(request, 'data/symptoms_list.html',
                  {'count': SymptomModel.objects.count(),
                   'symptoms': symptoms})


def symptom_add(request):
    if request.method == 'POST':
        print('---- inside POST')
        form = SymptomAddForm(request.POST, request.FILES)
        if form.is_valid():
            print('---- for is valid and ready to save')
            form.save()
            return redirect('data:symptoms-list')
    else:
        print('---- inside GET')
        form = SymptomAddForm

    return render(request, 'data/symptom_add.html', {'form': form})


def symptom_detail(request, symptom_id):
    symptom_data = get_object_or_404(SymptomModel, pk=symptom_id)
    return render(request, 'data/symptom_detail.html', {'symptom_detail': symptom_data})


def symptom_delete(request, symptom_id):
    symptom = SymptomModel.objects.get(pk=symptom_id)
    symptom.delete()
    symptoms = SymptomModel.objects.all()
    return redirect('data:symptoms-list')
    # return render(request, 'data/symptoms_list.html', {'symptoms': symptoms, 'count': SymptomModel.objects.count()})


def diseases_list(request):
    diseases = DiseaseModel.objects.all()
    return render(request, 'data/diseases_list.html',
                  {'count': DiseaseModel.objects.count(),
                   'diseases': diseases})


def disease_add(request):
    if request.method == 'POST':
        print('---- inside POST')
        form = DiseaseAddForm(request.POST)
        if form.is_valid():
            print('---- for is valid and ready to save')
            form.save()
            return redirect('data:diseases-list')
    else:
        print('---- inside GET')
        form = DiseaseAddForm

    return render(request, 'data/disease_add.html', {'form': form})


def disease_update(request, instance_id):
    if instance_id:
        disease_data = get_object_or_404(DiseaseModel, pk=instance_id)
        form = DiseaseEditForm(request.POST, instance=disease_data)
        if form.is_valid():
            form.save()
            return redirect('data:diseases-list')


def disease_detail(request, disease_id):
    disease_data = get_object_or_404(DiseaseModel, pk=disease_id)
    form = DiseaseEditForm(instance=disease_data)
    context = {
        'form': form,
        'disease_detail': disease_data 
    }
    return render(request, 'data/disease_detail.html', context)

def disease_predict(request, disease_id):
    disease_data = get_object_or_404(DiseaseModel, pk=disease_id)


def disease_delete(request, disease_id):
    disease = DiseaseModel.objects.get(pk=disease_id)
    disease.delete()
    diseases = DiseaseModel.objects.all()
    return redirect('data:diseases-list')
    # return render(request, 'data/diseases_list.html', {'diseases': diseases, 'count': DiseaseModel.objects.count()})

def disease_edit(request, disease_id):
    if request.method == 'POST':
        disease_data = get_object_or_404(DiseaseModel, pk=disease_id)
        form = DiseaseEditForm(request.POST, instance=disease_data)
        if form.is_valid():
            form.save()
            return redirect('data:diseases-list')
    else:
        disease_data = get_object_or_404(DiseaseModel, pk=disease_id)
        form = DiseaseEditForm(instance=disease_data)
    return render(request, 'data/disease_edit.html', {'form': form})


def disease_get(request):
    print('Here')
    if request.method == 'POST':
        print('in POST')
        form = DiseaseAddForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            instance.parameters_file
            patient_name = instance.patient.name
            file_obj = instance.parameters_file
            file_path = file_obj.path
            print(file_path)
            if os.path.isfile(file_path):
                print('check')
                file1 = open(file_path, 'r')
                line = file1.readlines()[0]
                parameters = line.split(',') #parameter values in list


                # Dictionary Object Code

                column_labels = ['fo', 'fhi', 'flo', 'jitter',
                'jitter_abs', 'rap', 'ppq', 'ddp', 'shimmer',
                'shimmer_db', 'shimmer_apq3', 'shimmer_apq5',
                'apq', 'dda', 'nhr', 'hnr', 'rpde', 'dfa',
                'spread1', 'spread2', 'd2', 'ppe',
                ]
                parameters_df = pd.DataFrame(columns=column_labels)
                a_series = pd. Series(parameters, index = parameters_df. columns)
                parameters_df = parameters_df. append(a_series, ignore_index=True)
                parameters_df.to_dict('index')
                d1 = dict(zip(column_labels, parameters))
                instance.save()
                #{'fo': 20.11}
                form = DiseaseEditForm(instance=instance, initial=d1)
                context = {
                    'form': form,
                    'instance': instance
                }
            return render(request, 'data/disease_add.html', context)
