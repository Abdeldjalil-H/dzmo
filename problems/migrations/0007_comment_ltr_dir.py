from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("problems", "0006_problemsubmission_ltr_dir"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="ltr_dir",
            field=models.BooleanField(default=False),
        ),
    ]
