from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import User, Contact
from .forms import RegisterForm, LoginForm, ProfileForm, ContactForm, CustomPasswordResetForm, CustomSetPasswordForm
from .tokens import account_activation_token
from django.views.generic import CreateView, ListView, UpdateView, TemplateView
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from homemart.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.utils.encoding import force_str, force_bytes
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login as auth_login


def activate(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.filter(pk=uid, is_active=False).first()

    if user is not None and account_activation_token.check_token(user, token):
        messages.success(request, 'Your profile is activated')
        user.is_active = True
        user.save()
        return redirect('/login/')
    else:
        messages.error(request, 'Your session is expired')
        return redirect('/')


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password1'])
        form.instance.save()

        subject = 'Qeydiyyatınızı təsdiqləyin'
        current_site = get_current_site(self.request)
        message = render_to_string('email/confirmation_email.html', {
            'user': form.instance,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(form.instance.pk)),
            'token': account_activation_token.make_token(form.instance),
        })
        from_email = EMAIL_HOST_USER
        to_email = self.request.POST['email']
        send_mail(
            subject,
            message,
            from_email,
            [to_email, ]
        )
        messages.success(
            self.request, ('Please confirm your email to complete registration.'))
        return redirect('login')


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    authentication_form = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super(CustomLoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super(CustomLoginView, self).form_valid(form)


class ForgetPasswordView(PasswordResetView):
    email_template_name = 'email/password_message.html'
    form_class = CustomPasswordResetForm
    template_name = 'password/forget_password.html'
    success_url = reverse_lazy('success_forget_password')


class ResetPasswordView(PasswordResetConfirmView):
    template_name = 'password/reset_password.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('success_reset_password')


class SuccessForgetPasswordView(TemplateView):
    template_name = "password/success_forget_password.html"


class SuccessResetPasswordView(TemplateView):
    template_name = "password/success_reset_password.html"


class ProfileView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    model = User
    template_name = 'profile.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk != self.kwargs['pk']:
            return redirect('error')
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return User.objects.filter(pk=self.kwargs['pk'])

    def form_valid(self, form):
        if form.cleaned_data['password1']:
            form.instance.set_password(form.cleaned_data['password1'])
            form.save()
            messages.success(
                self.request, 'Məlumatlarınız uğurla yeniləndi! Şifrəniz yeniləndiyi üçün yenidən giriş edin.')
            return redirect('login')
        messages.success(self.request, 'Məlumatlarınız uğurla yeniləndi!')
        response = super().form_valid(form)
        return response


class ProfileMobileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile-mobile.html'


class ContactView(LoginRequiredMixin, CreateView, ListView):
    form_class = ContactForm
    model = Contact
    context_object_name = "appeals"
    template_name = 'contact.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk != self.kwargs['pk']:
            return redirect('error')
        return super(ContactView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Contact.objects.filter(user__pk=self.kwargs['pk'])

    def form_valid(self, form):
        form.instance.user = User.objects.get(pk=self.kwargs['pk'])
        messages.success(self.request, 'Müraciətiniz uğurla göndərildi!')
        return super().form_valid(form)


def myorders(request):
    return render(request, "myorders.html")
