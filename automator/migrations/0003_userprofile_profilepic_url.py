# Generated by Django 3.2.6 on 2021-09-24 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automator', '0002_userprofile_github_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profilePic_url',
            field=models.TextField(default='https://rpgplanner.com/wp-content/uploads/2020/06/no-photo-available.png'),
        ),
    ]
