from django.shortcuts import render, get_object_or_404, redirect

from .forms import SymptomAddForm, DiseaseAddForm
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
        form = SymptomAddForm(request.POST)
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


def disease_detail(request, disease_id):
    disease_data = get_object_or_404(DiseaseModel, pk=disease_id)
    return render(request, 'data/disease_detail.html', {'disease_detail': disease_data})


def disease_delete(request, disease_id):
    disease = DiseaseModel.objects.get(pk=disease_id)
    disease.delete()
    diseases = DiseaseModel.objects.all()
    return redirect('data:diseases-list')
    # return render(request, 'data/diseases_list.html', {'diseases': diseases, 'count': DiseaseModel.objects.count()})
