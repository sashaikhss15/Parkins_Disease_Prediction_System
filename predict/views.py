# Create your views here.
import os
import datetime

import joblib
import pickle
import numpy as np

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa


from django.views.generic import View

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

import base64
import pdfkit
from django.core.files.uploadedfile import SimpleUploadedFile
def post_parameter_in_model(request):
    form = MyPredictForm(request.POST)
    if form.is_valid():
        parameters_list = []
        parameters_obj = form.cleaned_data['parameters']
        p = form.save()
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
        c = parameters_list

        #prediction code
        model_path = 'finalized_model.pkl'
        classifier = pickle.load(open(model_path, 'rb'))
        
        #prediction = classifier.predict(np.array([[199.228,209.512,192.091,0.00241,1.00E-05,0.00134,0.00138,0.00402,0.01015,0.089,0.00504,0.00641,0.00762,0.01513,0.00167,30.94,0.432439,0.742055,-7.682587,0.173319,2.103106,0.068501]]))[0]
        prediction = classifier.predict(np.array([parameters_list]))[0]
        print(type(prediction))
        print(prediction)
        # form = MyPredictForm
        parameters_name = ['fo', 'fhi','flo' ,
        'jitter', 'jitter_abs', 'rap', 'ppq', 'ddp' ,
        'shimmer', 'shimmer_db', 'shimmer_apq3' ,
        'shimmer_apq5', 'apq', 'dda', 'nhr' ,
        'hnr', 'rpde', 'dfa', 'spread1', 'spread2',
        'd2' , 'ppe']
        mlist = zip(parameters_name, parameters_list)
        patient_details = ['age', 'gender', 'height', 'weight']
        patient_values = [patientObj.age, patientObj.gender,
                        patientObj.height, patientObj.weight]
        pv = patient_values
        pc = zip(parameters_name, c)
        datalist = zip(patient_details, patient_values)
        datalist_copy = zip(patient_details, pv)
        # context = {
        #     'form': form,
        #     'prediction': prediction,
        #     'mlist': mlist,
        #     'patient_name': patientObj.name,
        #     'datalist': datalist,
        #     'is_visible': True
        # }
        
        pdf_base64 = None
        template = get_template("report.html")
        options = {"enable-local-file-access": None, "page-size": "letter"}
        html = template.render({
            'mlist': pc,
            'prediction': prediction,
            'patient_name': patientObj.name,
            'patient_age' : patientObj.age,
            'patient_gender' : patientObj.gender,
            'patient_height' : patientObj.height,
            'patient_weight' : patientObj.weight,
            'report_date' : datetime.datetime.now(),
            'datalist': datalist_copy,
            })
        pdf = pdfkit.from_string(html, "", options=options)
        pdf_base64 = base64.b64encode(pdf)
        pdf_obj = {}
        pdf_obj['name'] = '{}_report.pdf'.format(patientObj.name)
        pdf_obj['file'] = pdf_base64
        pdf_obj['content_type'] = 'application/pdf'
        pdf_url = decode_base64_file(pdf_obj)
        p.report_file = pdf_url
        p.save()
        # form = MyPredictForm()
        context = {
            'form': form,
            'prediction': prediction,
            'mlist': mlist,
            'patient_name': patientObj.name,
            'datalist': datalist,
            'is_visible': True,
            'p': p
        }
        return render(request, 'predict/parkinson_predict.html', context)


def decode_base64_file(base64_object):
    if base64_object != {}:
        try:
            lens = len(base64_object["file"])
            lenx = lens - (lens % 4 if lens % 4 else 4)
            decoded_file = SimpleUploadedFile(
                base64_object['name'],
                base64.b64decode(base64_object["file"][:lenx]),
                base64_object["content_type"]
            )
            return decoded_file
        except Exception as e:
            print("file exception", e)
            return Response({"detail": "Please pass the valid base64 object "
                                       "into the request."},
                            status=status.HTTP_400_BAD_REQUEST)

    return None



class Render:

    @staticmethod
    def render(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)


class Pdf(View):

    def get(self, request):
        print("In pdf")
        params = {
            'request': request
        }
        return Render.render('report.html', params)


import urllib
from django import template
register = template.Library()

@register.filter
def get_encoded_dict(data_dict):
    print(data_dict)
    return urllib.urlencode(data_dict)


def print_invoices(self, request):
    multiple_ids = request.query_params.get("multiple_invoices_uuid").split(",")
    invoices = self.get_queryset().filter(uuid__in=multiple_ids)
    pdf_base64 = None
    if invoices:
        template = get_template("invoice.html")
        options = {"enable-local-file-access": None, "page-size": "letter"}
        html = template.render(
            {
                "invoices": invoices,
            }
        )
        pdf = pdfkit.from_string(html, "", options=options)
        pdf_base64 = base64.b64encode(pdf)
    return Response({"data": pdf_base64})