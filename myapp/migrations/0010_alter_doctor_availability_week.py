# Generated by Django 4.0.5 on 2022-06-16 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_alter_doctor_availability_week_appoinment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor_availability',
            name='week',
            field=models.IntegerField(choices=[(2, 'TUESDAY'), (6, 'SATURDAY'), (4, 'THURSDAY'), (5, 'FRIDAY'), (1, 'MONDAY'), (3, 'WEDNESDAY')]),
        ),
    ]