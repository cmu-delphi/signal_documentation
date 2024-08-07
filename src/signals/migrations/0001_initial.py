# Generated by Django 4.2.3 on 2023-07-24 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('datasources', '0002_alter_sourcesubdivision_db_source'),
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Geography',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name', max_length=128, unique=True)),
            ],
            options={
                'verbose_name_plural': 'geographies',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Pathogen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name', max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SignalCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name', max_length=128, unique=True)),
            ],
            options={
                'verbose_name_plural': 'signal categories',
            },
        ),
        migrations.CreateModel(
            name='SignalType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name', max_length=128, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Signal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name', max_length=128)),
                ('display_name', models.CharField(help_text='Display Name', max_length=128)),
                ('active', models.BooleanField(default=False, help_text='Active')),
                ('short_description', models.TextField(blank=True, help_text='Short Description', max_length=500, null=True)),
                ('description', models.TextField(blank=True, help_text='Description', max_length=1000, null=True)),
                ('format', models.CharField(choices=[('raw', 'Raw'), ('percent', 'Percent'), ('fraction', 'Fraction'), ('count', 'Count'), ('per100k', 'Per 100K')], help_text='Format', max_length=128)),
                ('time_type', models.CharField(choices=[('day', 'Day'), ('week', 'Week')], help_text='Time type', max_length=128)),
                ('time_label', models.CharField(choices=[('day', 'Day'), ('date', 'Date'), ('week', 'Week')], help_text='Time label', max_length=128)),
                ('is_smoothed', models.BooleanField(default=False, help_text='Is Smoothed')),
                ('is_weighted', models.BooleanField(default=False, help_text='Is Weighted')),
                ('is_cumulative', models.BooleanField(default=False, help_text='Is Cumulative')),
                ('has_stderr', models.BooleanField(default=False, help_text='Has StdErr')),
                ('has_sample_size', models.BooleanField(default=False, help_text='Has Sample Size')),
                ('high_values_are', models.CharField(choices=[('bad', 'Bad'), ('good', 'Good'), ('neutral', 'Neutral')], help_text='High values are', max_length=128)),
                ('available_geography', models.ManyToManyField(help_text='Available geography', to='signals.geography')),
                ('base', models.ForeignKey(blank=True, help_text='Signal base', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='base_for', to='signals.signal')),
                ('category', models.ForeignKey(help_text='Signal Category', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='signals', to='signals.signalcategory')),
                ('links', models.ManyToManyField(help_text='Signal links', related_name='signals', to='base.link')),
                ('pathogen', models.ManyToManyField(help_text='Pathogen/Disease Area', related_name='signals', to='signals.pathogen')),
                ('signal_type', models.ManyToManyField(help_text='Signal Type', related_name='signals', to='signals.signaltype')),
                ('source', models.ForeignKey(help_text='Source Subdivision', on_delete=django.db.models.deletion.PROTECT, related_name='signals', to='datasources.sourcesubdivision')),
            ],
            options={
                'unique_together': {('name', 'source')},
            },
        ),
    ]
