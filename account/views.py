from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
# Create your views here.
from django.shortcuts import render

from account.forms import UserForm, PatientProfileForm, DoctorProfileForm, PatientEditProfileForm, DoctorEditProfileForm
from account.models import PatientProfileModel, DoctorProfileModel


def is_user_logged_in(request):
    if request.user.is_authenticated:
        print('user is already logged in : ' + request.user.username)
        return True
    print('no user found')
    return False


def index(request):
    print('------ index')
    form_profile = None
    is_user = False
    if is_user_logged_in(request):
        if request.user.username != 'anonymous' and request.user.username != 'admin':
            is_user = True
            print('------ valid user')
            try:
                profile = PatientProfileModel.objects.get(user=request.user)
                print('------ a patient')
                if request.method == 'POST':
                    print('-------- in patient POST')
                    form_profile = PatientEditProfileForm(request.POST)
                    if form_profile.is_valid():
                        print(f'-------- in patient post form valid = {form_profile.data}')
                        profile.age = form_profile.cleaned_data['age']
                        profile.state = form_profile.cleaned_data['state']
                        profile.city = form_profile.cleaned_data['city']
                        profile.height = form_profile.cleaned_data['height']
                        profile.weight = form_profile.cleaned_data['weight']
                        profile.blood_pressure = form_profile.cleaned_data['blood_pressure']
                        profile.gender = form_profile.cleaned_data['gender']
                        profile.smoker = form_profile.cleaned_data['smoker']
                        profile.save()
                else:
                    print('-------- in patient GET')
                    form_profile = PatientEditProfileForm(initial={
                        'name': profile.name,
                        'gender': profile.gender,
                        'age': profile.age,
                        'height': profile.height,
                        'weight': profile.weight,
                        'smoker': profile.smoker,
                        'blood_pressure': profile.blood_pressure,
                        'state': profile.state,
                        'city': profile.city,
                    })
            except PatientProfileModel.DoesNotExist:
                print('------ a doctor')
                profile = DoctorProfileModel.objects.get(user=request.user)
                if request.method == 'POST':
                    print('-------- in doc POST')
                    form_profile = DoctorEditProfileForm(request.POST, instance=request.user)
                    if form_profile.is_valid():
                        print(f'-------- in doc post form valid \n-------- {form_profile.data}')
                        print(f'-------- in doc post old age -------- {profile.age}')
                        profile.age = form_profile.cleaned_data['age']
                        profile.qualification = form_profile.cleaned_data['qualification']
                        profile.clinic_address = form_profile.cleaned_data['clinic_address']
                        profile.state = form_profile.cleaned_data['state']
                        profile.city = form_profile.cleaned_data['city']
                        profile.gender = form_profile.cleaned_data['gender']
                        profile.save()
                        print(f'-------- in doc post new age -------- {profile.age}')
                        print(f'-------- in doc post id \n-------- {profile.id}')
                        # form_profile.save()
                else:
                    print('-------- in doc GET')
                    form_profile = DoctorEditProfileForm(initial={
                        'name': profile.name,
                        'qualification': profile.qualification,
                        'gender': profile.gender,
                        'age': profile.age,
                        'clinic_address': profile.clinic_address,
                        'state': profile.state,
                        'city': profile.city,
                    })

    context = {
        'form': form_profile,
        'is_user': is_user
    }
    return render(request, 'account/index.html', context)


def logout_user(request):
    print(f'-------- logging out user = {request.user}')
    logout(request)
    # form = UserForm(request.POST or None)
    # context = {
    #     "form": form,
    # }
    return render(request, 'account/login.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # albums = Album.objects.filter(user=request.user)
                # return render(request, 'music/index.html', {'albums': albums})
                print(f'-------- user logged in = {request.user}')
                request.method = 'GET'
                return index(request)
            else:
                return render(request, 'account/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'account/login.html', {'error_message': 'Invalid login'})
    return render(request, 'account/login.html')


def register_patient(request):
    form = UserForm(request.POST or None)
    form_profile = PatientProfileForm(request.POST or None)

    if form.is_valid() and form_profile.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        confirm_password = form.cleaned_data['confirm_password']

        user.set_password(password)
        user.save()
        profile = form_profile.save(commit=False)
        profile.user = user
        profile.save()

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                return render(request, 'account/login.html')
    context = {
        'form_user': form,
        'form_profile': form_profile
    }
    return render(request, 'account/register_patient.html', context)


def register_doctor(request):
    form = UserForm(request.POST or None)
    form_profile = DoctorProfileForm(request.POST or None)

    if form.is_valid() and form_profile.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        confirm_password = form.cleaned_data['confirm_password']

        user.set_password(password)
        user.save()
        profile = form_profile.save(commit=False)
        profile.user = user
        profile.save()

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                return render(request, 'account/login.html')
    context = {
        'form_user': form,
        'form_profile': form_profile
    }
    return render(request, 'account/register_doctor.html', context)
