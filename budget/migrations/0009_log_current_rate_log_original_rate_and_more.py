# Generated by Django 4.0.4 on 2022-08-02 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0008_alter_driver_driver_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='current_rate',
            field=models.DecimalField(decimal_places=2, default=7.0, max_digits=9),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='log',
            name='original_rate',
            field=models.DecimalField(decimal_places=2, default='7', max_digits=9),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='driver',
            name='driver_type',
            field=models.CharField(choices=[('O88', 'Owner operator - 88%'), ('O85', 'Owner operator - 85%'), ('C30', 'Company driver - 30%'), ('C35', 'Company driver - 35%'), ('L**', 'Lease operator'), ('R**', 'Rental operator')], max_length=3),
        ),
    ]
