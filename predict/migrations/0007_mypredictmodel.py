# Generated by Django 3.2 on 2021-05-08 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_auto_20210503_2313'),
        ('predict', '0006_alter_predictmodel_symptoms'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyPredictModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parameters', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data.diseasemodel')),
            ],
        ),
    ]
