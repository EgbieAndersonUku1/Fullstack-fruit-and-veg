# Generated by Django 5.1 on 2024-09-06 02:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0013_remove_userprofile_billing_addresses_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='giftcard',
            old_name='name',
            new_name='card_type',
        ),
    ]