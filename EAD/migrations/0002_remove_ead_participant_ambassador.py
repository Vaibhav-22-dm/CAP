# Generated by Django 3.2.5 on 2021-07-11 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EAD', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ead_participant',
            name='ambassador',
        ),
    ]
