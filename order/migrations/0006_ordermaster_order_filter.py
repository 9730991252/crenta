# Generated by Django 5.0.2 on 2024-03-03 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_order_detail_price_order_detail_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermaster',
            name='order_filter',
            field=models.IntegerField(default=True),
        ),
    ]