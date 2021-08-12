from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import logout,authenticate,login
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import force_text,force_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode

from .models import User, Profile
from .forms import (UserRegisterForm, LoginForm, ChangePasswordForm,
    ResetPasswordValidateEmailForm, ForgetPasswordForm)
from .tokens import acount_confirm_token
from .utils import get_next_redirect, send_email



def verification_message(request, user, template):
	site=get_current_site(request)
	uid=urlsafe_base64_encode(force_bytes(user.pk))
	token=acount_confirm_token.make_token(user)
	message=render_to_string(template,{
		"user": user.get_emailname(),
		"uid": uid,
		"token": token,
		"domain": site.domain,
		'from': settings.DEFAULT_FROM_EMAIL
	})
	return message


class AuthenticationView(FormView):
    template_name = 'account/authentication.html'
    extra_context = {
        'title': 'Login or Register',
    }
    form_class = UserRegisterForm
    login_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["login"] = self.login_class()
        context["register"] = self.form_class()

        return context
    

    def get(self, request, *args, **kwargs):
        # Check if user is already logged in
        if request.user.is_authenticated:
            return redirect('main:home')

        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        request = self.request
        context = self.get_context_data()

        # Identify the form that was submitted
        submit = request.POST.get('submit')

        if submit == 'register':
            form = self.form_class(request.POST)
            if form.is_valid():
                user = form.save()
                subject=f"Wellbos Verification"
                message = verification_message(request, user, "account/activation_email.html")
                sent=user.email_user(subject,message)
                messages.success(request, f'You account is successfully created. A link was sent to your email {user.email}, use the link to verify you account.')
                return redirect('account:authentication')
            
            context["register"] = form

        elif submit == 'login':
            form = self.login_class(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')

                user = authenticate(request, username=email, password=password)
                if user:
                    login(request, user)
                    messages.success(request, f'Welcome, {user.get_emailname()}')
                    
                    # Check if a next page is available, else redirect to homes page
                    next = get_next_redirect(request)
                    if next:
                        return next

                    return redirect('main:home')
                else:
                    messages.warning(request, 'Please, you have to verify your email before you can login.')
                    return redirect('account:authentication')
            
            context["login"] = form

        messages.warning(request, 'Invalid info.')
        
        return render(request, self.template_name, context)


def activate_email(request, uidb64, token):
	try:
		uid=force_text(urlsafe_base64_decode(uidb64))
		user=User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user=None
	if user!=None and acount_confirm_token.check_token(user,token):
		user.active=True
		user.save()

		messages.success(request,f'{user.email}, your email is now verified successfully, you can now login')
		return redirect('account:authentication')
	else:
		messages.warning(request, 'This link is invalid')
		return redirect('account:authentication')


class ChangePassword(LoginRequiredMixin, UpdateView):
    template_name = 'account/change_password.html'
    extra_context = {
        'title': 'Change Password'
    }
    form_class = ChangePasswordForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form'] = self.form_class()

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        request = self.request
        context = self.get_context_data()

        cloned = request.POST.copy()
        cloned['user_pk'] = request.user.pk

        form = self.form_class(cloned)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your password is successfully changed, please login with your new password')
            return redirect('account:logout')
        else:
            messages.warning(request, 'You did not properly fill the change password form.')
        
        context['form'] = form
        
        return render(request, self.template_name, context)


class ResetPasswordFormPage(FormView):
    template_name = 'account/reset_password_form.html'
    extra_context = {
        'title': 'Reset Password',
    }
    form_class = ResetPasswordValidateEmailForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form'] = self.form_class()

        if request.user.is_authenticated:
            logout(request)

        return render(request, self.template_name, context)
    
    def post(self, *args, **kwargs):
        request = self.request

        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            user = User.objects.filter(email__exact=email).first()

            if user:
                # Send the reset link to user
                subject = "Wellbos Password Reset"
                message = verification_message(request, user, "account/password_reset.html")
                user.email_user(subject,message)

            messages.success(request, 'Your password reset link has been emailed to you if your account is registered')

            return redirect('account:authentication')
        
        context = self.get_context_data()
        context['form'] = form

        return render(request, self.template_name, context)


class ResetPasswordVerify(FormView):
    template_name = 'account/reset_password_page.html'
    extra_context = {
        'title': 'Reset your password',
    }
    form_class = ForgetPasswordForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form'] = self.form_class()

        # Get uidb4 and token from kwargs
        uidb64 = self.kwargs.get('uidb64')
        token = self.kwargs.get('token')

        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)

        if acount_confirm_token.check_token(user,token):
            messages.success(request,'You can now change your password with the form below')
        else:
            messages.warning(request, 'This password reset link is invalid.')
            return redirect('account:password_reset')

        return render(request, self.template_name, context)
    
    def post(self, *args, **kwargs):
        request = self.request

        # Get uidb4 from kwargs and get the user instance
        uidb64 = self.kwargs.get('uidb64')
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)

        form = self.get_form_class()
        form = form(request.POST)

        if form.is_valid():
            # Get the cleaned password and set the user password
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()

            if request.user.is_authenticated:
                logout(request)

            messages.success(request, 'You password has been successfully changed, now login with your new password')
            return redirect('account:authentication')
        
        context = self.get_context_data()
        context['form'] = form

        return render(request, self.template_name, context)

def Logout(request):
    logout(request)
    messages.success(request, 'Logged out')
    return redirect('account:authentication')