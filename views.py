import json
import logging

from django.contrib import auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist

from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import csrf

from django.urls import reverse
from django.views import View

from . import forms
from .models import Course, CustomUser

logger = logging.getLogger(__name__)

async def home(request):
    """Home method....."""
    template_name = 'main/index.html'
    context = {'banner': 'Main Page', 'title': 'Main Page'}
    # await test(request)
    return render(request, template_name, context=context)

def validate_register_form(request):
    """AJAX Register Form validation....."""
    context = {}
    if request.is_ajax:
        form = forms.SignUpForm(request.POST)

        if form.is_valid():
            context.update({'is_valid': True})
            logger.debug('Sign Up form has been validated....')

        logger.debug('form is not valid. Input Errors: %s' % form.errors)
        return JsonResponse(context)

def validate_login_form(request):
    """AJAX Login Form validation....."""
    context = {}

    if request.is_ajax:

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                context.update({'is_valid': True})
            return JsonResponse(context, status=200)

        except ObjectDoesNotExist:
            logger.debug('user has been specified wrong data')

    return JsonResponse(context)

class AuthRegisterView(View):
    """Registration View....."""
    context = {}
    template_name = 'main/sign_up.html'

    def get(self, request):
        self.context.update(csrf(request))

        self.context['form'] = forms.SignUpForm()
        self.context['banner'] = 'Registration'

        return render(request, self.template_name, context=self.context)

    def post(self, request):
        form = forms.SignUpForm(request.POST)
        if form.is_valid():

            new_user = CustomUser.objects.create_user(**form.cleaned_data)
            login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')

        return HttpResponseRedirect(reverse('main:home'))

class AuthLoginView(View):
    """Authentication View....."""
    context = {}
    template_name = 'main/sign_in.html'

    def get(self, request):
        self.context.update(csrf(request))
        self.context['form'] = forms.SignInForm()

        self.context['banner'] = 'Login In'
        return render(request, self.template_name, context=self.context)

    def post(self, request):

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return HttpResponseRedirect(reverse('main:home'))

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)

    print('user is not authenticated anymore.....')
    return redirect('/')








