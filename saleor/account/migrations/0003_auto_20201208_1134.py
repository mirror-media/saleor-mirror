# Generated by Django 3.1.2 on 2020-12-08 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20201203_0216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='company_name',
        ),
        migrations.AddField(
            model_name='address',
            name='gender',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]