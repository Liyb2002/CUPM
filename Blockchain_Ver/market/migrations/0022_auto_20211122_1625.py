# Generated by Django 3.2.6 on 2021-11-22 21:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('market', '0021_auto_20211121_2303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teamgame',
            name='away_token',
        ),
        migrations.RemoveField(
            model_name='teamgame',
            name='home_token',
        ),
        migrations.AlterField(
            model_name='trade',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trades', to='market.teamgame'),
        ),
        migrations.AlterField(
            model_name='trade',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trades', to='market.team'),
        ),
        migrations.AlterField(
            model_name='trade',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trades', to=settings.AUTH_USER_MODEL),
        ),
    ]
