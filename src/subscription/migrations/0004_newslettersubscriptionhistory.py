# Generated by Django 5.1 on 2024-10-25 21:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0003_subscribednewslettersubscription_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsletterSubscriptionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255)),
                ('action', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('frequency', models.CharField(blank=True, choices=[('d', 'Daily'), ('w', 'Weekly'), ('BW', 'Bi-weekly'), ('m', 'Monthly'), ('q', 'Quarterly')], max_length=2, null=True)),
                ('reason_for_unsubscribing', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscription_history', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Newsletter Subscription History',
                'verbose_name_plural': 'Newsletter Subscription Histories',
            },
        ),
    ]