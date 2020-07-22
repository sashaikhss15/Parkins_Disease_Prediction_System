from django.shortcuts import render

from account.models import DoctorProfileModel


def is_user_logged_in(request):
    if request.user.is_authenticated:
        print('user is already logged in : ' + request.user.username)
        return True
    print('no user found')
    return False


def index(request):
    is_doctor = False
    if is_user_logged_in(request):
        try:
            doctor = DoctorProfileModel.objects.get(user=request.user)
            is_doctor = True
            print(f'----------- Doc here : {doctor.name}')
        except DoctorProfileModel.DoesNotExist:
            pass
    return render(request, 'index.html', {'is_doctor': is_doctor})
