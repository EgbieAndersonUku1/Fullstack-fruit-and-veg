# Generated by Django 5.1 on 2025-01-06 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_product_is_returnable'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='recommendation',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]