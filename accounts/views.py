from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse


def login(request):
    response_data = {}
    response_data['url'] = request.POST['next']
    username = request.POST['username']
    password = request.POST['password']
    if request.method == 'POST' and request.is_ajax:
        try:
            get_user = User.objects.get(username=username)
            if get_user.check_password(password):
                user = auth.authenticate(
                    username=username, password=password)
                if user is not None:
                    auth.login(request, user)
                    response_data['login'] = "success"
                else:
                    response_data['login'] = "nouser"
            else:
                response_data['login'] = "password"
        except:
            response_data['login'] = "nouser"
    else:
        response_data['login'] = "failed"

    return HttpResponse(JsonResponse(response_data))


def signup(request):
    response_data = {}
    response_data['url'] = request.POST['next']
    if request.method == 'POST' and request.is_ajax:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(email=request.POST['email'])
                response_data['register'] = "email"
                return HttpResponse(JsonResponse(response_data))
            except:
                pass
            try:
                user = User.objects.get(username=request.POST['username'])
                response_data['register'] = "user"
                return HttpResponse(JsonResponse(response_data))
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'],
                                                email=request.POST['email'])
                auth.login(request, user)
                response_data['register'] = "success"
                return HttpResponse(JsonResponse(response_data))
        else:
            response_data['register'] = "password"
            return HttpResponse(JsonResponse(response_data))
    else:
        response_data['register'] = "failed"
        return HttpResponse(JsonResponse(response_data))


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
