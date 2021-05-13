# Generated by Django 2.2.5 on 2020-01-14 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DiseaseModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disease_name', models.CharField(max_length=100)),
                ('disease_description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SymptomModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symptom_name', models.CharField(max_length=100)),
                ('symptom_description', models.TextField()),
            ],
        ),
    ]
