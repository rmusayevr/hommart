from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from django.urls import reverse

class User(AbstractBaseUser, PermissionsMixin):
    genders = {
        ("Qadın", "Qadın"),
        ("Kişi", "Kişi"),
    }

    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(_('full name'), max_length=100)
    phone_number = models.CharField(_('phone number'), max_length=10)
    gender = models.CharField(_('gender'), max_length=30, choices=genders)
    extra_phone_number = models.CharField(_('extra phone number'), max_length=10, null=True, blank=True)
    city_number = models.CharField(_('city number'), max_length=10, null=True, blank=True)
    birthday = models.DateField(_('birthday'), max_length=50, null=True, blank=True)
    passport_number = models.CharField(_('passport number'), max_length=30, null=True, blank=True)
    address = models.TextField(_('address'), null=True, blank=True)
    address_link = models.TextField(_('address link'), null=True, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=False)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_superuser = models.BooleanField(_('superuser'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.full_name
    
class Contact(models.Model):
    statuses = {
        ("Şikayət", "Şikayət"),
        ("Təklif", "Təklif")
    }

    status = models.CharField(max_length=30, choices=statuses)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_contact')
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def get_absolute_url(self):
        return reverse('contact', kwargs={'pk': self.user.pk})

    def __str__(self):
        return self.user
