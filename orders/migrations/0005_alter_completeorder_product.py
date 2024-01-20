# Generated by Django 5.0.1 on 2024-01-20 07:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_completeorder_product'),
        ('products', '0003_product_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='completeorder',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.product', verbose_name='محصول'),
        ),
    ]
