# Generated by Django 2.1.8 on 2019-09-25 06:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_auto_20190915_0749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_data',
            name='enddate',
            field=models.DateField(default=datetime.date(2019, 10, 25)),
        ),
    ]
