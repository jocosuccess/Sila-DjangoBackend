# Generated by Django 2.1.8 on 2019-08-21 17:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_account_data_registrationdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_data',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
