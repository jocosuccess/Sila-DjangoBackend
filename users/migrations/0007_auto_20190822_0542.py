# Generated by Django 2.1.8 on 2019-08-22 05:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_data_relation'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='account_data',
            name='enddate',
            field=models.DateField(default=datetime.date(2019, 9, 21)),
        ),
    ]