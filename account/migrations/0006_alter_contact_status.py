# Generated by Django 3.2.20 on 2023-07-14 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_contact_status_alter_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='status',
            field=models.CharField(choices=[('Təklif', 'Təklif'), ('Şikayət', 'Şikayət')], max_length=30),
        ),
    ]