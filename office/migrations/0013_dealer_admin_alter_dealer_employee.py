# Generated by Django 5.0.2 on 2024-02-26 08:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0012_remove_dealer_added_by_dealer_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='dealer',
            name='admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='office.admin'),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='office.employee'),
        ),
    ]
