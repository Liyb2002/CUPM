# Generated by Django 3.2.6 on 2021-09-09 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0009_auto_20210909_1954'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamgame',
            name='positionIdHi',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='teamgame',
            name='positionIdLo',
            field=models.TextField(default=''),
        ),
    ]
