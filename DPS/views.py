from django.shortcuts import render

from account.models import DoctorProfileModel
from account.views import index as account_index


def is_user_logged_in(request):
    if request.user.is_authenticated:
        print('user is already logged in : ' + request.user.username)
        return True
    print('no user found')
    return False


def index(request):
    '''
        method will check user logged in or not at http://127.0.0.1:8000/
    '''
    is_doctor = False
    if is_user_logged_in(request):
        try:
            doctor = DoctorProfileModel.objects.get(user=request.user)
            if doctor:
                is_doctor = True
                print(f'----------- Doc here : {doctor.name}')
                return render(request, 'index.html', {'is_doctor': is_doctor})
                # dashboad page
        except DoctorProfileModel.DoesNotExist:
            pass

    else:
        form_profile = None
        is_user = False
        context = {
            'form': form_profile,
            'is_user': is_user
        }
        print('account render')
        return render(request, 'account/index.html', context)# login page
