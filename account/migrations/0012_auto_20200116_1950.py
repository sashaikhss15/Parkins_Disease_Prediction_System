# Generated by Django 2.2.5 on 2020-01-16 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20200116_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorprofilemodel',
            name='clinic_address',
            field=models.TextField(blank=True, default='', help_text='If Any', max_length=300, null=True),
        ),
    ]
