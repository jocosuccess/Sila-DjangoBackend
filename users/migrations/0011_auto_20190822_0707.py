# Generated by Django 2.1.8 on 2019-08-22 07:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20190822_0706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='payment_datetime',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
