from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("problems", "0005_auto_20210102_2249"),
    ]

    operations = [
        migrations.AddField(
            model_name="problemsubmission",
            name="ltr_dir",
            field=models.BooleanField(default=False),
        ),
    ]
