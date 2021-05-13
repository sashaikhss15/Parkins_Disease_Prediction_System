# Create your views here.
import os

import joblib
import pickle
import numpy as np

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect

from DPS import settings
from account.models import PatientProfileModel, DoctorProfileModel
from data.models import DiseaseModel
from data.forms import DiseaseAddForm
from predict.forms import PredictForm, MyPredictForm
from predict.models import PredictedDiseaseModel, PredictModel, MyPredictModel


def is_user_logged_in(request):
    if request.user.is_authenticated:
        print('user is already logged in : ' + request.user.username)
        return True
    print('no user found')
    return False


def index(request):
    logged_in_status = False
    form = PredictForm(request.POST or None)
    name = 'Anonymous'
    username = 'anonymous'
    if is_user_logged_in(request):
        username = request.user.username
        try:
            name = PatientProfileModel.objects.get(user=request.user).name
            logged_in_status = True
        except PatientProfileModel.DoesNotExist:
            pass
        print(f'-------- loading prediction form for username [{username}] name [{name}]')

    if request.method == 'POST':
        if form.is_valid():
            feeding_data = list()
            for single in form.Meta.model.Symptoms:
                if single[0] in form.cleaned_data.get('symptoms'):
                    print(f'single = {single[0]}')
                    feeding_data.append(1)
                else:
                    feeding_data.append(0)
            print(f'final feeding list = {feeding_data}')
            dt = joblib.load(os.path.join(settings.MODEL_ROOT, 'my_model_for_dps'))
            y_diagnosis = dt.predict([feeding_data])
            y_pred_2 = dt.predict_proba([feeding_data])
            print(f'y_diagnosis = {y_diagnosis}')
            print(f'y_pred_2 = {y_pred_2}')
            print(f'Name of the infection = {y_diagnosis[0]} , confidence score of : = {y_pred_2.max() * 100}')
            form.Meta.model.disease_name = y_diagnosis[0]
            form.Meta.model.prediction_confidence = y_pred_2.max
            predict_model_obj = form.save()

            PredictedDiseaseModel.objects.create(predict_model=predict_model_obj, disease_name=y_diagnosis[0],
                                                 prediction_confidence=(y_pred_2.max() * 100))
            return redirect('predict:result', predict_model_id=predict_model_obj.id)
        else:
            print(f'------ predict form is not valid')
    else:
        form = PredictForm(initial={'patient_name': name, 'patient_username': username})
        print(f'new predict form with fields {form.fields}')
    return render(request, 'predict/index.html',
                  {'form': form, 'logged_in_status': logged_in_status, 'is_doctor': False})


def result(request, predict_model_id):
    logged_in_status = False
    doctors = list()
    if is_user_logged_in(request):
        logged_in_status = True
        try:
            model = PatientProfileModel.objects.get(user=request.user)
            try:
                doctor_models = DoctorProfileModel.objects.filter(state__iexact=model.state,
                                                                  city__iexact=model.city).values_list('name',
                                                                                                       'clinic_address')
            except DoctorProfileModel.DoesNotExist:
                doctor_models = DoctorProfileModel.objects.all().values_list('name', 'clinic_address')
        except PatientProfileModel.DoesNotExist:
            doctor_models = DoctorProfileModel.objects.all().values_list('name', 'clinic_address')
        for doc in doctor_models:
            print(f'--------- doc = {doc[0]}\n{doc[1]}')
            doctors.append(doc)

    predicted_disease_model = PredictedDiseaseModel.objects.get(predict_model=predict_model_id)
    prediction_model = PredictModel.objects.get(pk=predict_model_id)
    print(f'----------predict_model_id = {predict_model_id}')
    print(f'----------predicted_disease_model = {type(PredictModel.Symptoms)}')
    symptoms = list()
    for single in PredictModel.Symptoms:
        if single[0] in prediction_model.symptoms:
            symptoms.append(single[1])

    print(f'----------- = {symptoms}')
    return render(request, 'predict/result.html', {'data': predicted_disease_model,
                                                   'symptoms': symptoms,
                                                   'logged_in_status': logged_in_status,
                                                   'doctor_list': doctors})


def approvals(request):
    is_doctor = False
    is_user = False
    if is_user_logged_in(request):
        try:
            doctor = DoctorProfileModel.objects.get(user=request.user)
            is_doctor = True
            print(f'----------- Doc here : {doctor.name}')
        except DoctorProfileModel.DoesNotExist:
            pass
    predicted_data = list()
    patient_data = list()
    data = list()
    models = PredictedDiseaseModel.objects.filter(is_approved=False).values_list()
    print(f'----------- approvals = {str(models)}')
    for single in models:
        predicted_data.append(single)
        x = PredictModel.objects.get(pk=single[0])
        patient_data.append(x)
        print(f' ------- checking indexing = {single[2]}')
        print(f' ------- checking indexing (P) = {x.patient_name}')
        if x.patient_username != 'anonymous' and x.patient_username != 'admin':
            print(f'----------- user with username[{x.patient_username}]')
            is_user = True
            user = User.objects.get(username=x.patient_username)
            profile_details = PatientProfileModel.objects.get(user=user)
            my_dict = {
                'id': single[0],
                'name': x.patient_name,
                'disease': single[2],
                'confidence': single[3],
                'symptoms': x.symptoms,
                'gender': profile_details.gender,
                'age': profile_details.age,
                'smoker': profile_details.smoker,
                'height': profile_details.height,
                'weight': profile_details.weight,
                'blood_pressure': profile_details.blood_pressure,
                'is_user': is_user,
            }
        else:
            my_dict = {
                'id': single[0],
                'name': x.patient_name,
                'disease': single[2],
                'confidence': single[3],
                'symptoms': x.symptoms,
                'is_user': is_user,
            }
        data.append(my_dict)

    print(f'----------- patient = {str(patient_data)}')

    return render(request, 'predict/approvals.html', {'data': data, 'is_doctor': is_doctor})


def approve(request, approval_id):
    model = PredictedDiseaseModel.objects.get(pk=approval_id)
    print(f'---------- approval model {str(model)}')
    try:
        model.is_approved = True
        model.approved_by = DoctorProfileModel.objects.get(user=request.user).name
        model.save()
    except (KeyError, PredictedDiseaseModel.DoesNotExist):
        return JsonResponse({'success': False})

    return approvals(request)


def reject(request, reject_id):
    model = PredictedDiseaseModel.objects.get(pk=reject_id)
    print(f'---------- approval model {str(model)}')
    try:
        model.is_approved = True
        model.rejected_by = DoctorProfileModel.objects.get(user=request.user).name
        model.save()
    except (KeyError, PredictedDiseaseModel.DoesNotExist):
        return JsonResponse({'success': False})

    return approvals(request)


def history(request):
    data = list()
    models = PredictModel.objects.filter(patient_username=request.user.username).order_by('-id').values_list()
    print(f'------------ history models of type = {type(models)} = {str(models)}')
    for single in models:
        disease_model = PredictedDiseaseModel.objects.get(pk=single[0])
        if disease_model.is_approved:
            if disease_model.approved_by is not None and disease_model.approved_by != '':
                my_dict = {
                    'disease_name': disease_model.disease_name,
                    'confidence': disease_model.prediction_confidence,
                    'symptoms': single[3],
                    'approved_by': disease_model.approved_by,
                    'key': 2,
                }
            else:
                my_dict = {
                    'disease_name': disease_model.disease_name,
                    'confidence': disease_model.prediction_confidence,
                    'symptoms': single[3],
                    'rejected_by': disease_model.rejected_by,
                    'key': 3,
                }
        else:
            my_dict = {
                'disease_name': disease_model.disease_name,
                'confidence': disease_model.prediction_confidence,
                'symptoms': single[3],
                'key': 1,
            }
        data.append(my_dict)
        print(f'------ dict = {my_dict}')
    return render(request, 'predict/history.html', {'data': data, })


###
#parkinson_predict
###

def parkinson_predict(request):
    if is_user_logged_in(request):
        print('In predict')
        print('---- inside GET')
        form = MyPredictForm
        return render(request, 'predict/parkinson_predict.html', {'form': form})

def post_parameter_in_model(request):
    form = MyPredictForm(request.POST)
    if form.is_valid():
        parameters_list = []
        parameters_obj = form.cleaned_data['parameters']
        print(type(parameters_obj))

        print(type(parameters_obj.patient))
        print(parameters_obj.id)
        print(parameters_obj.patient)
        #instance = MyPredictModel.objects.get(parameters=parameters_obj)
        #list(Article.objects.values_list('comment_id', flat=True).distinct()

        patientObj = PatientProfileModel.objects.get(id=parameters_obj.patient.id)

        print(type(patientObj.name))

        qs = list(DiseaseModel.objects.filter(id=parameters_obj.id).values_list().distinct())[0]
        print(qs)
        for i in qs:
            if type(i) is float:
                parameters_list.append(i)
        
        print(parameters_list)


        #prediction code
        model_path = '/home/coda/aq_project/disease-prediction-system/finalized_model.pkl'
        classifier = pickle.load(open(model_path, 'rb'))
        
        #prediction = classifier.predict(np.array([[199.228,209.512,192.091,0.00241,1.00E-05,0.00134,0.00138,0.00402,0.01015,0.089,0.00504,0.00641,0.00762,0.01513,0.00167,30.94,0.432439,0.742055,-7.682587,0.173319,2.103106,0.068501]]))[0]
        prediction = classifier.predict(np.array([parameters_list]))[0]
        print(type(prediction))
        print(prediction)
        form = MyPredictForm
        parameters_name = ['fo', 'fhi','flo' ,
        'jitter', 'jitter_abs', 'rap', 'ppq', 'ddp' ,
        'shimmer', 'shimmer_db', 'shimmer_apq3' ,
        'shimmer_apq5', 'apq', 'dda', 'nhr' ,
        'hnr', 'rpde', 'dfa', 'spread1', 'spread2',
        'd2' , 'ppe']
        mlist = zip(parameters_name, parameters_list)
        context = {
            'form': form,
            'prediction': prediction,
            'mlist': mlist,
            'patient_name': patientObj.name,
            'is_visible': True
        }
        return render(request, 'predict/parkinson_predict.html', context)
