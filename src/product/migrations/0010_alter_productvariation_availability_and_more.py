# Generated by Django 5.1 on 2025-01-04 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_product_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariation',
            name='availability',
            field=models.CharField(choices=[('IS', 'In Stock'), ('OO', 'Out of Stock'), ('PO', 'Pre-order')], default='IS', max_length=3),
        ),
        migrations.AlterField(
            model_name='productvariation',
            name='height',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Height (in cm)'),
        ),
        migrations.AlterField(
            model_name='productvariation',
            name='length',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Length (in cm)'),
        ),
        migrations.AlterField(
            model_name='productvariation',
            name='size',
            field=models.CharField(max_length=50, verbose_name='Size (e.g. s, m, l, xl)'),
        ),
        migrations.AlterField(
            model_name='productvariation',
            name='width',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Width (in cm)'),
        ),
    ]