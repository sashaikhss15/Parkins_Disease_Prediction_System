# Generated by Django 2.2.5 on 2020-01-18 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0002_auto_20200118_1942'),
    ]

    operations = [
        migrations.RenameField(
            model_name='predicteddiseasemodel',
            old_name='is_approved_by',
            new_name='approved_by',
        ),
    ]
