# Generated by Django 2.1.3 on 2018-12-09 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_follow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='title',
        ),
    ]