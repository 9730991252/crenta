# Generated by Django 5.0.6 on 2024-08-18 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0002_rename_employee_office_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Store_employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('mobile', models.IntegerField()),
                ('pin', models.IntegerField()),
                ('status', models.IntegerField(default=1)),
                ('added_date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
