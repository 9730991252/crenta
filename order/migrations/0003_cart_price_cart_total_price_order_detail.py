# Generated by Django 5.0.2 on 2024-03-03 04:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0013_dealer_admin_alter_dealer_employee'),
        ('order', '0002_ordermaster'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='price',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='total_price',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.CreateModel(
            name='Order_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marketing_employee_name', models.CharField(blank=True, max_length=100, null=True)),
                ('office_employee_name', models.CharField(blank=True, max_length=100, null=True)),
                ('store_employee_name', models.CharField(blank=True, max_length=100, null=True)),
                ('product_name', models.CharField(max_length=100)),
                ('category', models.CharField(default=True, max_length=100)),
                ('qty', models.IntegerField(default=1)),
                ('type', models.CharField(blank=True, max_length=100, null=True)),
                ('orderfilter', models.IntegerField(default=True)),
                ('status', models.IntegerField(choices=[('1', 'in stock'), ('0', 'out of stock')], default=1)),
                ('ordered_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('dealer', models.ForeignKey(default=True, on_delete=django.db.models.deletion.PROTECT, to='office.dealer')),
                ('product', models.ForeignKey(blank=True, default=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='office.product')),
            ],
        ),
    ]
