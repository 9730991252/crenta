# Generated by Django 5.0.6 on 2024-06-24 11:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0030_batch_delete_add_new_batch'),
        ('qr_code', '0003_in_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='in_stock',
            name='product',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.PROTECT, to='office.product'),
        ),
    ]
