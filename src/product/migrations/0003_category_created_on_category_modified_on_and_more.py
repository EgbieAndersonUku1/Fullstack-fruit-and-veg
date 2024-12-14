# Generated by Django 5.1 on 2024-12-08 01:43

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_brand_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='modified_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='manufacturer',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='manufacturer',
            name='modified_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]