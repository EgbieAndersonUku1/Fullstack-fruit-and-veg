# Generated by Django 5.1 on 2024-10-22 15:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='newslettersubscription',
            name='email',
            field=models.EmailField(default=None, max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='newslettersubscription',
            name='frequency',
            field=models.CharField(choices=[('d', 'Daily'), ('w', 'Weekly'), ('BW', 'Bi-weekly'), ('m', 'Monthly'), ('q', 'Quarterly')], default='m', max_length=2),
        ),
        migrations.AlterField(
            model_name='newslettersubscription',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='newsletter_subscriptions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='newslettersubscription',
            index=models.Index(fields=['user'], name='subscriptio_user_id_bb5b64_idx'),
        ),
    ]