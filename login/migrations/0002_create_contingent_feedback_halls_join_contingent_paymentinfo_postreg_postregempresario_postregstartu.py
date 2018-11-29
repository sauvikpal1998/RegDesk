# Generated by Django 2.0.5 on 2018-06-23 06:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='create_contingent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_id', models.CharField(max_length=255)),
                ('emp_pass', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0)),
                ('comments', models.TextField(max_length=300, null=True)),
                ('download', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Halls',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.TextField(max_length=150)),
                ('capacity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='join_contingent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_id1', models.CharField(max_length=255)),
                ('emp_pass1', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('size', models.IntegerField(default=1)),
                ('txn_id', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostReg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostRegEmpresario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acco', models.BooleanField(default=True)),
                ('size', models.IntegerField(default=1)),
                ('name2', models.CharField(max_length=100, null=True)),
                ('email2', models.EmailField(max_length=100, null=True)),
                ('mobile2', models.BigIntegerField(null=True)),
                ('name3', models.CharField(max_length=100, null=True)),
                ('email3', models.EmailField(max_length=100, null=True)),
                ('mobile3', models.BigIntegerField(null=True)),
                ('name4', models.CharField(max_length=100, null=True)),
                ('email4', models.EmailField(max_length=100, null=True)),
                ('mobile4', models.BigIntegerField(null=True)),
                ('name5', models.CharField(max_length=100, null=True)),
                ('email5', models.EmailField(max_length=100, null=True)),
                ('mobile5', models.BigIntegerField(null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostRegStartup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('details', models.TextField(max_length=600, null=True)),
                ('website', models.URLField(max_length=100, null=True)),
                ('size', models.IntegerField(null=True)),
                ('events', models.CharField(max_length=100)),
                ('startup_seedfund', models.BooleanField(default=False)),
                ('startup_stage', models.CharField(max_length=100, null=True)),
                ('intern_number', models.IntegerField(default=0)),
                ('intern_stipend', models.CharField(max_length=100, null=True)),
                ('intern_location', models.CharField(max_length=100, null=True)),
                ('intern_profile', models.CharField(max_length=200, null=True)),
                ('intern_duration', models.CharField(max_length=100, null=True)),
                ('intern_description', models.CharField(max_length=100, null=True)),
                ('epitch_sector', models.CharField(max_length=255, null=True)),
                ('epitch_problem', models.TextField(max_length=600, null=True)),
                ('epitch_market', models.TextField(max_length=600, null=True)),
                ('epitch_revenue', models.TextField(max_length=600, null=True)),
                ('epitch_compete', models.TextField(max_length=600, null=True)),
                ('epitch_funds', models.TextField(max_length=600, null=True)),
                ('epitch_deck', models.URLField(null=True)),
                ('pexpo_type', models.CharField(max_length=20, null=True)),
                ('pexpo_details', models.TextField(max_length=600, null=True)),
                ('pexpo_demo', models.URLField(null=True)),
                ('comeet_idea', models.BooleanField(default=False)),
                ('comeet_skill_set', models.TextField(max_length=600, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Travel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]