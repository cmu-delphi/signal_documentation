# Generated by Django 4.2.10 on 2024-02-15 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasources', '0003_datasource_created_datasource_modified_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='datasource',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='sourcesubdivision',
            options={'ordering': ['name']},
        ),
    ]
