# Generated by Django 4.1.3 on 2022-12-24 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('participant', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='is_paid',
        ),
    ]