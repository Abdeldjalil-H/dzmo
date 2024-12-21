from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("problems", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="problemsubmission",
            name="file",
            field=models.FileField(blank=True, null=True, upload_to="students_subs"),
        ),
    ]
