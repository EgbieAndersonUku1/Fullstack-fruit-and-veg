# Generated by Django 5.1 on 2024-10-15 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testimonal', '0007_alter_testimonial_ratings'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonial',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='testimonial',
            name='user_image',
            field=models.URLField(blank=True, null=True, verbose_name='Profile image url'),
        ),
    ]
