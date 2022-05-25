# Generated by Django 4.0.3 on 2022-05-25 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('samsara_id', models.IntegerField(null=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('odometer', models.IntegerField(default=0)),
                ('latitude', models.DecimalField(decimal_places=8, max_digits=11, null=True)),
                ('longitude', models.DecimalField(decimal_places=8, max_digits=11, null=True)),
                ('headingDegrees', models.SmallIntegerField(null=True)),
                ('speed', models.SmallIntegerField(null=True)),
                ('location', models.CharField(max_length=120, null=True)),
            ],
        ),
    ]
