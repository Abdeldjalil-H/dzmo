from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("problems", "0003_auto_20210101_1831"),
    ]

    operations = [
        migrations.AlterField(
            model_name="problemsubmission",
            name="submited_on",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
