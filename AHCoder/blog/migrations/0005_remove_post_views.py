# Generated by Django 3.0.8 on 2020-07-08 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='views',
        ),
    ]
