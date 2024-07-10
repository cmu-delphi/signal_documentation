# Generated by Django 4.2.10 on 2024-06-07 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('signals', '0012_remove_signal_licence_signal_license_delete_licence'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signal',
            name='signal_type',
        ),
        migrations.AddField(
            model_name='signal',
            name='signal_type',
            field=models.ForeignKey(help_text='Source Type', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='signals', to='signals.signaltype'),
        ),
    ]
