# Generated by Django 5.1 on 2024-10-13 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_user_last_token_generated_on'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='banuser',
            options={'verbose_name': 'All banned users', 'verbose_name_plural': 'All banned users'},
        ),
    ]
