# Generated by Django 2.2.5 on 2020-01-15 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20200115_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofilemodel',
            name='age',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
