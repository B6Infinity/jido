# Generated by Django 3.2.6 on 2021-10-19 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automator', '0007_alter_automation_github_repo_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='online',
            field=models.BooleanField(default=False),
        ),
    ]