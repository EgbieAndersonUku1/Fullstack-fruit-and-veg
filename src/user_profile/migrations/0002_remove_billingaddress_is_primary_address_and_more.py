# Generated by Django 5.1 on 2024-09-22 01:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billingaddress',
            name='is_primary_address',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='is_primary_address',
        ),
    ]
