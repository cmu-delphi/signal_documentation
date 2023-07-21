# Generated by Django 4.2.3 on 2023-07-21 13:51

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signals', '0003_alter_signal_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signal',
            name='base',
        ),
        migrations.AddField(
            model_name='signal',
            name='group',
            field=models.ForeignKey(help_text='Group', on_delete=django.db.models.deletion.PROTECT, related_name='signals', to='signals.signalgroup'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='signalgroup',
            name='base',
            field=models.ForeignKey(help_text='Base Signal', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='base_for', to='signals.signal'),
        ),
    ]
