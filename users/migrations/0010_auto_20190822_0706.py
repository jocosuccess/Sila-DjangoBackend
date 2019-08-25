# Generated by Django 2.1.8 on 2019-08-22 07:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_transactions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactions',
            name='date',
        ),
        migrations.AddField(
            model_name='transactions',
            name='payment_datetime',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]