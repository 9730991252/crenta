# Generated by Django 5.0.2 on 2024-05-23 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0026_alter_dealer_dealer_mobile'),
    ]

    operations = [
        migrations.AddField(
            model_name='sell_product',
            name='bach_number',
            field=models.CharField(max_length=100, null=True),
        ),
    ]