import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tests", "0009_auto_20210820_2308"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="testanswer",
            name="mark",
        ),
        migrations.RemoveField(
            model_name="testanswer",
            name="uploaded_files",
        ),
        migrations.AddField(
            model_name="testanswer",
            name="marks",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.SmallIntegerField(), null=True, size=None
            ),
        ),
    ]
