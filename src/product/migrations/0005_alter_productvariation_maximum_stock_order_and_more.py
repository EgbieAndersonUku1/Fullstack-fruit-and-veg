# Generated by Django 5.1 on 2024-12-08 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_category_options_remove_product_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariation',
            name='maximum_stock_order',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='productvariation',
            name='minimum_stock_order',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='productvariation',
            name='size',
            field=models.CharField(max_length=50, verbose_name='Size e.g s, m, l, xl'),
        ),
    ]