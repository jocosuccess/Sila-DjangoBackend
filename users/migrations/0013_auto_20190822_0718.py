# Generated by Django 2.1.8 on 2019-08-22 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20190822_0715'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='plan',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='amount_paid',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='currency_paid',
            field=models.CharField(max_length=60),
        ),
    ]
