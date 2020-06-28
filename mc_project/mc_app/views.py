from django.shortcuts import render
from . import forms

#
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):

    context = {'name': 'hello world'}

    return render(request, 'webpage/index.html', context=context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):

    registered = False

    if request.method == 'POST':
        user_form = forms.UserForm(data=request.POST)
        profile_form = forms.UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = forms.UserForm()
        profile_form = forms.UserProfileInfoForm()

    context = {'registered': registered, 'user_form': user_form, 'profile_form': profile_form}

    return render(request, 'webpage/registration.html', context)



def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('passwrd')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                print('ACCOUNT NOT ACTIVE!')
        else:
            print('Someone tried to login but failed')
            print('Username: {}, Password: {}'.format(username, password))
            return HttpResponse('username not found, please register first!')

    return render(request, 'webpage/login.html')
