# Generated by Django 4.2.9 on 2024-01-22 03:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='user_password_rest_tokrn',
            new_name='user_password_rest_token',
        ),
    ]
