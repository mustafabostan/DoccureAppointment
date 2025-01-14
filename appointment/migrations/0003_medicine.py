# Generated by Django 5.1.4 on 2024-12-27 00:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0002_patient_examinationrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medicines', to='appointment.doctor')),
            ],
        ),
    ]
