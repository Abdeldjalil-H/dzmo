from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("problems", "0002_auto_20201225_2253"),
        ("accounts", "0002_studentprogress"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studentprogress",
            name="last_submissions",
            field=models.ManyToManyField(blank=True, to="problems.ProblemSubmission"),
        ),
    ]
