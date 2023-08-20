# Generated by Django 4.1.9 on 2023-06-09 15:19

import account.managers
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('full_name', models.CharField(max_length=100, verbose_name='full name')),
                ('phone_number', models.CharField(max_length=10, verbose_name='phone number')),
                ('gender', models.CharField(choices=[('Kişi', 'Kişi'), ('Qadın', 'Qadın')], max_length=30, verbose_name='gender')),
                ('extra_phone_number', models.CharField(blank=True, max_length=10, null=True, verbose_name='extra phone number')),
                ('city_number', models.CharField(blank=True, max_length=10, null=True, verbose_name='city number')),
                ('birthday', models.DateField(blank=True, max_length=50, null=True, verbose_name='birthday')),
                ('passport_number', models.CharField(blank=True, max_length=30, null=True, verbose_name='passport number')),
                ('address', models.TextField(blank=True, null=True, verbose_name='address')),
                ('address_link', models.TextField(blank=True, null=True, verbose_name='address link')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('is_active', models.BooleanField(default=False, verbose_name='active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', account.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Şikayət', 'Şikayət'), ('Təklif', 'Təklif')], max_length=30)),
                ('comment', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_contact', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
        ),
    ]
