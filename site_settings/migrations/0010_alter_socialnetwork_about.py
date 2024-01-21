# Generated by Django 5.0.1 on 2024-01-21 03:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0009_alter_socialnetwork_name_alter_socialnetwork_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialnetwork',
            name='about',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='socials', to='site_settings.aboutme', verbose_name='مدل درباره من'),
        ),
    ]
