# Generated by Django 2.0.5 on 2018-06-16 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='session_type',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='data',
            name='contingent',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
