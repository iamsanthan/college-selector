# Generated by Django 3.0.3 on 2020-06-22 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firstweb', '0017_chatmessage_thread'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thread',
            name='first',
        ),
        migrations.RemoveField(
            model_name='thread',
            name='second',
        ),
        migrations.DeleteModel(
            name='ChatMessage',
        ),
        migrations.DeleteModel(
            name='Thread',
        ),
    ]
