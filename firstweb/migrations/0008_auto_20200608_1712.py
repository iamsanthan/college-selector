# Generated by Django 3.0.3 on 2020-06-08 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firstweb', '0007_auto_20200607_2303'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='username',
            new_name='user',
        ),
    ]
