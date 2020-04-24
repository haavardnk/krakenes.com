from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponsePermanentRedirect
from django.contrib.auth.decorators import login_required


@login_required(login_url=('account_login'))
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return HttpResponsePermanentRedirect(reverse('home'))

@login_required(login_url=('account_login'))
def profile(request):
    user = request.user
    return render(request, 'account/profile.html', {'user':user})
