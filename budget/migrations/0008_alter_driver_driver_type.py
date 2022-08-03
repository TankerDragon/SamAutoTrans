# Generated by Django 4.0.4 on 2022-07-22 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0007_alter_driver_driver_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='driver_type',
            field=models.CharField(choices=[('O88', 'Owner operator - 88%'), ('O88', 'Owner operator - 85%'), ('C30', 'Company driver - 30%'), ('C35', 'Company driver - 35%'), ('L**', 'Lease operator'), ('R**', 'Rental operator')], max_length=3),
        ),
    ]
