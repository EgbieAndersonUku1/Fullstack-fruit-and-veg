# Generated by Django 5.1 on 2024-11-06 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0010_newslettersubscription_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newslettersubscription',
            name='subscribed_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]