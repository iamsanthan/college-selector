# Generated by Django 3.0.3 on 2020-06-14 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firstweb', '0010_stud'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stud',
            old_name='college',
            new_name='clgname',
        ),
    ]
