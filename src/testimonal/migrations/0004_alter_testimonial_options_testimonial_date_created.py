# Generated by Django 5.1 on 2024-10-13 11:57

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testimonal', '0003_rename_testimonal_testimonial_approvedtestimonial_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testimonial',
            options={'verbose_name': 'Testimonial', 'verbose_name_plural': 'All Testimonials'},
        ),
        migrations.AddField(
            model_name='testimonial',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]