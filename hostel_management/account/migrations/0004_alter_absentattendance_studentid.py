# Generated by Django 4.1.7 on 2023-06-19 17:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_absentattendance_dateabsent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='absentattendance',
            name='studentId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
