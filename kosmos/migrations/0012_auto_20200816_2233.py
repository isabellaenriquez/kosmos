# Generated by Django 3.0.6 on 2020-08-17 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kosmos', '0011_user_has_notifications'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='has_notifications',
        ),
        migrations.AddField(
            model_name='user',
            name='notifications',
            field=models.PositiveIntegerField(default=0),
        ),
    ]