# Generated by Django 5.0 on 2024-02-02 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signals', '0004_rename_format_signal_format_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='signalcategory',
            options={'ordering': ['name'], 'verbose_name_plural': 'signal categories'},
        ),
    ]
