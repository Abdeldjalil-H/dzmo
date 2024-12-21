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
