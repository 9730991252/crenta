# Generated by Django 5.0.6 on 2024-06-25 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qr_code', '0006_voucher_num_verify_by_voucher_num_verify_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='voucher_num',
            name='verify_date',
            field=models.DateTimeField(null=True),
        ),
    ]
