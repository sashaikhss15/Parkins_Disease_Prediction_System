# Generated by Django 2.2.5 on 2020-01-19 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predict', '0003_auto_20200118_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predicteddiseasemodel',
            name='approved_by',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
