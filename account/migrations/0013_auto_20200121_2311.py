# Generated by Django 2.2.5 on 2020-01-21 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_auto_20200116_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientprofilemodel',
            name='height',
            field=models.CharField(default='0', help_text='5 ft. 6 in.', max_length=20),
        ),
    ]
