# Generated by Django 5.1 on 2024-10-05 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_token_generated_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
