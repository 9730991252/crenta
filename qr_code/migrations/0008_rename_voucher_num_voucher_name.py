# Generated by Django 5.0.6 on 2024-06-25 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0030_batch_delete_add_new_batch'),
        ('qr_code', '0007_voucher_num_verify_date'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Voucher_num',
            new_name='Voucher_name',
        ),
    ]
