# Generated by Django 2.0.5 on 2018-11-28 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_remove_contingent_contingent_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='contingent',
            name='link',
            field=models.CharField(default='01', max_length=100),
        ),
    ]
