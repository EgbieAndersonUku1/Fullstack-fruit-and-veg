# Generated by Django 5.1 on 2024-10-25 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0004_newslettersubscriptionhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='newslettersubscriptionhistory',
            name='title',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]
