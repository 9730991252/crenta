# Generated by Django 5.0.6 on 2024-06-24 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qr_code', '0004_in_stock_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='in_stock',
            name='tag_number',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]
