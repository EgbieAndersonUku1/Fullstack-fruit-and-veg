# Generated by Django 5.1 on 2025-01-06 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_product_recommendation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufacturer',
            name='contact_num',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]