# Generated by Django 2.0.5 on 2018-06-14 11:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('designation', models.CharField(default='Faculty', max_length=100)),
                ('city', models.CharField(max_length=255)),
                ('college', models.CharField(max_length=255)),
                ('mobile', models.IntegerField()),
                ('email', models.EmailField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Contingent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contingent_id', models.CharField(max_length=15)),
                ('captcha', models.CharField(max_length=100)),
                ('size', models.IntegerField(default=5)),
                ('stage', models.IntegerField(default=1)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('college', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='registration.College')),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('category', models.CharField(max_length=50)),
                ('stage', models.SmallIntegerField(default=0)),
                ('gender', models.CharField(max_length=10)),
                ('mobile', models.BigIntegerField()),
                ('tshirt', models.CharField(max_length=1)),
                ('city', models.CharField(max_length=100)),
                ('college', models.CharField(default=None, max_length=150)),
                ('contingent', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NewCollege',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('gender', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=150)),
                ('year_of_study', models.CharField(max_length=150)),
                ('mobile', models.IntegerField()),
                ('city', models.CharField(max_length=150)),
                ('college', models.CharField(max_length=150)),
                ('contact_dean', models.CharField(max_length=255)),
                ('contact_ecell', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=150, null=True)),
            ],
        ),
    ]
