# Generated by Django 4.2.11 on 2024-04-27 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_product_sizes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sizes',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
