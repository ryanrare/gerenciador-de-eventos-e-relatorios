# Generated by Django 5.0.4 on 2024-04-24 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_remove_event_update_at_event_updated_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='event',
            name='update_at',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='deleted_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]
