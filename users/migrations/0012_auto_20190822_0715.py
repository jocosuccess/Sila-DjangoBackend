# Generated by Django 2.1.8 on 2019-08-22 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20190822_0707'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='amount_paid',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='transactions',
            name='currency_paid',
            field=models.CharField(default='USD', max_length=60),
        ),
    ]
