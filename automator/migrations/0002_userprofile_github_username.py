# Generated by Django 3.2.6 on 2021-09-24 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='github_username',
            field=models.CharField(blank=True, max_length=39, null=True),
        ),
    ]
