# Generated by Django 3.2.6 on 2021-10-11 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automator', '0006_automation_readme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='automation',
            name='github_repo_URL',
            field=models.CharField(max_length=170),
        ),
    ]
