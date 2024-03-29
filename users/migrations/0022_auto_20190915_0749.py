# Generated by Django 2.1.8 on 2019-09-15 07:49

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_account_data_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_data',
            name='enddate',
            field=models.DateField(default=datetime.date(2019, 10, 15)),
        ),
        migrations.AlterField(
            model_name='reports',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user_data'),
        ),
        migrations.AlterField(
            model_name='reports',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user_data',
            name='account_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
