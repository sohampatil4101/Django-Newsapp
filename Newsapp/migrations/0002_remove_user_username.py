# Generated by Django 4.1.5 on 2023-07-26 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Newsapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
