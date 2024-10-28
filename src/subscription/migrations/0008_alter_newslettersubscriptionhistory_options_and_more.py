# Generated by Django 5.1 on 2024-10-28 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0007_newslettersubscriptionhistory_unsubscribed_on_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newslettersubscriptionhistory',
            options={'verbose_name': 'Subscription History', 'verbose_name_plural': 'Subscription Histories'},
        ),
        migrations.AlterModelOptions(
            name='subscribednewslettersubscription',
            options={'verbose_name': 'Subscribed Subscription', 'verbose_name_plural': 'Subscribed Subscriptions'},
        ),
        migrations.AlterModelOptions(
            name='unsubscribednewslettersubscription',
            options={'verbose_name': 'Unsubscribed Subscription', 'verbose_name_plural': 'Unsubscribed Subscriptions'},
        ),
        migrations.AlterField(
            model_name='newslettersubscription',
            name='reason_for_unsubscribing',
            field=models.TextField(blank=True, null=True),
        ),
    ]
