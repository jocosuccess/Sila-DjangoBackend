# Generated by Django 2.1.8 on 2019-09-02 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_auto_20190902_0143'),
    ]

    operations = [
        migrations.AddField(
            model_name='account_data',
            name='language',
            field=models.CharField(default='en', max_length=40),
        ),
    ]
