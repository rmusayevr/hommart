# Generated by Django 4.1.9 on 2023-07-05 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_contact_status_alter_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='status',
            field=models.CharField(choices=[('Şikayət', 'Şikayət'), ('Təklif', 'Təklif')], max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('Kişi', 'Kişi'), ('Qadın', 'Qadın')], max_length=30, verbose_name='gender'),
        ),
    ]
