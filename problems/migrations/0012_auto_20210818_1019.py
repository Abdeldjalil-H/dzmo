# Generated by Django 3.1.3 on 2021-08-18 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0011_auto_20210803_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemsubmission',
            name='solution',
            field=models.TextField(blank=True, null=True),
        ),
    ]
