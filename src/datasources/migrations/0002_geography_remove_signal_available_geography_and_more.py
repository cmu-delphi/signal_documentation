# Generated by Django 4.2 on 2023-04-24 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasources', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Geography',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name', max_length=128, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='signal',
            name='available_geography',
        ),
        migrations.AddField(
            model_name='signal',
            name='available_geography',
            field=models.ManyToManyField(help_text='Available geography', to='datasources.geography'),
        ),
    ]
