# Generated by Django 2.0.5 on 2018-06-23 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_create_contingent_feedback_halls_join_contingent_paymentinfo_postreg_postregempresario_postregstartu'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postregempresario',
            name='email2',
        ),
        migrations.RemoveField(
            model_name='postregempresario',
            name='email3',
        ),
        migrations.RemoveField(
            model_name='postregempresario',
            name='email4',
        ),
        migrations.RemoveField(
            model_name='postregempresario',
            name='email5',
        ),
        migrations.RemoveField(
            model_name='postregempresario',
            name='mobile2',
        ),
        migrations.RemoveField(
            model_name='postregempresario',
            name='mobile3',
        ),
        migrations.RemoveField(
            model_name='postregempresario',
            name='mobile4',
        ),
        migrations.RemoveField(
            model_name='postregempresario',
            name='mobile5',
        ),
        migrations.RemoveField(
            model_name='postregempresario',
            name='name2',
        ),
        migrations.RemoveField(
            model_name='postregempresario',
            name='name3',
        ),
        migrations.RemoveField(
            model_name='postregempresario',
            name='name4',
        ),
        migrations.RemoveField(
            model_name='postregempresario',
            name='name5',
        ),
        migrations.AddField(
            model_name='postreg',
            name='fav_startup',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='postreg',
            name='inspiration',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='postreg',
            name='profile',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='postreg',
            name='stage',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='postreg',
            name='startup',
            field=models.BooleanField(default=False),
        ),
    ]
