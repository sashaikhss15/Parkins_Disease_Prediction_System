# Generated by Django 2.2.5 on 2020-01-20 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0004_auto_20200119_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='predicteddiseasemodel',
            name='rejected_by',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
