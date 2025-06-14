# Generated by Django 5.2.2 on 2025-06-09 07:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admin_actions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Research_articles',
            fields=[
                ('research_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('link', models.CharField(max_length=200)),
                ('admin_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_actions.admin')),
            ],
            options={
                'verbose_name': 'Research Article',
                'verbose_name_plural': 'Research Articles',
            },
        ),
    ]
