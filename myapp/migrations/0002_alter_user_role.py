# Generated by Django 4.0.5 on 2022-06-14 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, default='none', max_length=150, null=True),
        ),
    ]
