# Generated by Django 4.2.3 on 2023-07-31 17:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2023, 7, 31, 17, 44, 24, 912457, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='link',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
