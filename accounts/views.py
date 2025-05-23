# from allauth.account.views import SignupView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import FormView

from accounts.forms import CustomSignupForm, CustomLogInForm
from publications.models import HumanInfo, Email


# Create your views here.
class CustomSignupView(FormView):
    form_class = CustomSignupForm
    template_name = 'account/signup.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            city = form.cleaned_data['city']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email,
                                     password=password1)
            h = HumanInfo.objects.create(first_name=first_name, last_name=last_name, city=city)
            Email.objects.create(human_info=h, address=email)

        return redirect('login')


class CustomLogInView(FormView):
    form_class = CustomLogInForm
    template_name = 'account/login.html'

