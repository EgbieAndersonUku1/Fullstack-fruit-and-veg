# Generated by Django 5.1 on 2024-10-25 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0005_newslettersubscriptionhistory_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='newslettersubscription',
            name='title',
            field=models.CharField(default='General Newsletter', max_length=255),
        ),
    ]
