# Generated by Django 5.0.2 on 2024-03-05 06:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0015_alter_sell_product_dealer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sell_product',
            name='dealer',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.PROTECT, to='office.dealer'),
        ),
    ]
