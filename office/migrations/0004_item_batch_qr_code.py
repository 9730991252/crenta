# Generated by Django 5.0.6 on 2024-08-18 05:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0003_store_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('sr_num', models.IntegerField(null=True)),
                ('added_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.IntegerField(default=1)),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='office.office_employee')),
            ],
        ),
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sr_num', models.IntegerField()),
                ('batch_name', models.CharField(max_length=200)),
                ('date', models.DateField(auto_now_add=True)),
                ('in_employee', models.ForeignKey(default=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='office.store_employee')),
                ('item', models.ForeignKey(default=True, on_delete=django.db.models.deletion.PROTECT, to='office.item')),
            ],
        ),
        migrations.CreateModel(
            name='Qr_code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_number', models.IntegerField(unique=True)),
                ('in_status', models.IntegerField(default=0)),
                ('out_status', models.IntegerField(default=0)),
                ('generate_date', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('batch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='office.batch')),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='office.office_employee')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='office.item')),
            ],
        ),
    ]
