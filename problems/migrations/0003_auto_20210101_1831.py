# Generated by Django 3.1.3 on 2021-01-01 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("problems", "0002_auto_20201225_2253"),
    ]

    operations = [
        migrations.AlterField(
            model_name="problemsubmission",
            name="submited_on",
            field=models.DateTimeField(blank=True),
        ),
    ]
