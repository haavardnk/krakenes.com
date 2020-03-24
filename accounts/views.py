from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponsePermanentRedirect, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required


def login(request):
    response_data = {}
    if request.method == 'POST' and request.is_ajax:
        response_data['url'] = request.POST['next']
        username = request.POST['username']
        password = request.POST['password']
        try:
            get_user = User.objects.get(username=username)
            if get_user.check_password(password):
                user = auth.authenticate(
                    username=username, password=password)
                auth.login(request, user)
                response_data['login'] = "success"
            else:
                response_data['login'] = "password"
        except:
            response_data['login'] = "nouser"
    else:
        response_data['login'] = "failed"

    return HttpResponse(JsonResponse(response_data))

@login_required(login_url=('home'))
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return HttpResponsePermanentRedirect(reverse('home'))
