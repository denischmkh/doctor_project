# Generated by Django 5.1.7 on 2025-03-19 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser_app', '0009_alter_doctor_address_alter_doctor_clinic_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='name',
            field=models.TextField(null=True),
        ),
    ]
