# Generated by Django 5.1 on 2024-10-17 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testimonal', '0010_alter_testimonial_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testimonial',
            name='title',
            field=models.CharField(max_length=20),
        ),
    ]