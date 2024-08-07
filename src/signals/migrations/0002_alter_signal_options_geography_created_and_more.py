# Generated by Django 4.2.3 on 2023-07-31 17:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signals', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='signal',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='geography',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2023, 7, 31, 17, 44, 40, 707597, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='geography',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='pathogen',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2023, 7, 31, 17, 44, 44, 129432, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pathogen',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='signal',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2023, 7, 31, 17, 44, 46, 984631, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='signal',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='signalcategory',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2023, 7, 31, 17, 44, 49, 753035, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='signalcategory',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='signaltype',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2023, 7, 31, 17, 44, 51, 932486, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='signaltype',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
