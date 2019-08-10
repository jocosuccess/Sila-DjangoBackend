# Generated by Django 2.2.4 on 2019-08-10 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='custom_verification_code',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=70, null=True, unique=True)),
                ('code', models.IntegerField(unique=True)),
            ],
        ),
    ]
