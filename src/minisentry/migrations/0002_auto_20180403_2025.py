# Generated by Django 2.0.3 on 2018-04-03 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('minisentry', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['timestamp']},
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ['last_seen']},
        ),
    ]