from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("problems", "0012_auto_20210818_1019"),
        ("tasks", "0002_auto_20210815_1116"),
        ("control", "0003_correctorsnotif"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="correctorsnotif",
            name="num_corrected_subs",
        ),
        migrations.RemoveField(
            model_name="correctorsnotif",
            name="num_old_subs",
        ),
        migrations.AddField(
            model_name="correctorsnotif",
            name="new_subs",
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="correctorsnotif",
            name="url",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="correctorsnotif",
            name="notif_each",
            field=models.SmallIntegerField(default=5),
        ),
        migrations.CreateModel(
            name="Submissions",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "last_correct_subs",
                    models.ManyToManyField(
                        blank=True,
                        related_name="_submissions_last_correct_subs_+",
                        to="problems.ProblemSubmission",
                    ),
                ),
                (
                    "problems_subs",
                    models.ManyToManyField(
                        blank=True,
                        related_name="_submissions_problems_subs_+",
                        to="problems.ProblemSubmission",
                    ),
                ),
                (
                    "tasks_subs",
                    models.ManyToManyField(
                        blank=True,
                        related_name="_submissions_tasks_subs_+",
                        to="tasks.TaskProblemSubmission",
                    ),
                ),
            ],
        ),
    ]
