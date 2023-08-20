from django import forms
from .models import User, Contact
from homemart.settings import DATE_INPUT_FORMATS
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm


class RegisterForm(UserCreationForm):
    genders = {
        ("Qadın", "Qadın"),
        ("Kişi", "Kişi"),
    }

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control inputs',
                                                                                    'placeholder': 'Parol'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control inputs',
                                                                                            'placeholder': 'Parolu təkrarla'}))
    gender = forms.ChoiceField(label="Gender", widget=forms.RadioSelect(
        attrs={'class': 'form-check-input'}), choices=genders)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number',
                  'gender', 'password1', 'password2']

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control inputs',
                                                'placeholder': "Ad Soyad"}),
            'email': forms.EmailInput(attrs={'class': 'form-control inputs',
                                             'placeholder': "Mail adresi"}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control inputs',
                                            'placeholder': "Telefon nömrəsi"}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]

        if password1 != password2:
            raise forms.ValidationError("Şifrələr eyni deyil!")
        return password2

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        if phone_number[:3] == "050" or phone_number[:3] == "051" or phone_number[:3] == "055" or phone_number[:3] == "010" or phone_number[:3] == "099" or phone_number[:3] == "070" or phone_number[:3] == "077":
            return phone_number
        else:
            raise forms.ValidationError("Düzgün telefon nömrəsi daxil edin.")


class LoginForm(AuthenticationForm):

    username = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control ps-4',
            'placeholder': 'Mail adresin'
        }))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control ps-4',
            'placeholder': 'Parol'
        }))

    remember_me = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={
            'class': 'form-check-input',
            'placeholder': 'Parol'
        }), required=False)


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email Address", widget=forms.EmailInput(
        attrs={
            'class': 'form-control ps-4 py-2 w-100',
            'placeholder': 'Mail adresi'
        }))


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(required=True, label='New Password',
                                    widget=forms.PasswordInput(
                                        attrs={
                                            'class': 'form-control ps-4 py-2 w-100',
                                            'placeholder': 'Yeni parol'
                                        }))
    new_password2 = forms.CharField(required=True, label='Confirm New Password',
                                    widget=forms.PasswordInput(
                                        attrs={
                                            'class': 'form-control ps-4 py-2 w-100',
                                            'placeholder': 'Yeni parol təkrarla'
                                        }))

    def clean_new_password2(self):
        new_password1 = self.cleaned_data["new_password1"]
        new_password2 = self.cleaned_data["new_password2"]

        if new_password1 != new_password2:
            raise forms.ValidationError("Şifrələr eyni deyil!")
        return new_password2


class ProfileForm(forms.ModelForm):
    genders = {
        ("Qadın", "Qadın"),
        ("Kişi", "Kişi"),
    }

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control inputs'}), required=False)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control inputs'}), required=False)
    gender = forms.ChoiceField(label="Gender", widget=forms.RadioSelect(
        attrs={'class': 'form-check-input'}), choices=genders)
    birthday = forms.DateField(label="Birthday", input_formats=DATE_INPUT_FORMATS, widget=forms.DateInput(
        attrs={'class': 'form-control inputs'}), required=False)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number', 'extra_phone_number', 'city_number', 'birthday',
                  'passport_number', 'password1', 'password2', 'address', 'address_link', 'gender']

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control inputs'}),
            'email': forms.EmailInput(attrs={'class': 'form-control inputs'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control inputs'}),
            'extra_phone_number': forms.TextInput(attrs={'class': 'form-control inputs'}),
            'city_number': forms.TextInput(attrs={'class': 'form-control inputs'}),
            'passport_number': forms.TextInput(attrs={'class': 'form-control inputs'}),
            'address': forms.Textarea(attrs={'class': 'form-control inputs'}),
            'address_link': forms.TextInput(attrs={'class': 'form-control inputs'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]

        if password1 != password2:
            raise forms.ValidationError("Şifrələr eyni deyil!")
        return password2

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        if phone_number:
            if phone_number[:3] == "050" or phone_number[:3] == "051" or phone_number[:3] == "055" or phone_number[:3] == "010" or phone_number[:3] == "099" or phone_number[:3] == "070" or phone_number[:3] == "077":
                return phone_number
            else:
                raise forms.ValidationError(
                    "Düzgün telefon nömrəsi daxil edin.")

    def clean_extra_phone_number(self):
        extra_phone_number = self.cleaned_data["extra_phone_number"]
        if extra_phone_number:
            if extra_phone_number[:3] == "050" or extra_phone_number[:3] == "051" or extra_phone_number[:3] == "055" or extra_phone_number[:3] == "010" or extra_phone_number[:3] == "099" or extra_phone_number[:3] == "070" or extra_phone_number[:3] == "077":
                return extra_phone_number
            else:
                raise forms.ValidationError(
                    "Düzgün telefon nömrəsi daxil edin!")

    def clean_passport_number(self):
        passport_number = self.cleaned_data["passport_number"]
        if passport_number:
            if passport_number[:2] == "AA" and len(passport_number) == 9:
                return passport_number
            elif passport_number[:3] != "AZE" and len(passport_number) == 11:
                return passport_number
            else:
                raise forms.ValidationError(
                    "Şəxsiyyət vəsiqəsinin nömrəsini düzgün daxil edin!")


class ContactForm(forms.ModelForm):
    statuses = {
        ("Şikayət", "Şikayət"),
        ("Təklif", "Təklif")
    }

    status = forms.ChoiceField(label="Status", widget=forms.Select(
        attrs={'class': 'form-select px-4 py-2 fw-bold'}), choices=statuses)

    class Meta:
        model = Contact
        fields = ['status', 'comment']

        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control p-3',
                                             'placeholder': "Fikrini yaz",
                                             'rows': 3})
        }
