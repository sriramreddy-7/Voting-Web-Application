# Generated by Django 4.2.1 on 2024-04-04 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_choice_poll_pollvote_choice_poll'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='stopped',
            field=models.BooleanField(default=False),
        ),
    ]