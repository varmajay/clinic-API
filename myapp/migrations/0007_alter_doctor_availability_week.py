# Generated by Django 4.0.5 on 2022-06-15 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_doctor_availability'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor_availability',
            name='week',
            field=models.CharField(choices=[(1, 'TUESDAY'), (5, 'SATURDAY'), (0, 'MONDAY'), (2, 'WEDNESDAY'), (4, 'FRIDAY'), (3, 'THURSDAY')], max_length=15),
        ),
    ]