import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lessons", "0001_initial"),
        ("problems", "0001_initial"),
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="StudentProgress",
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
                ("points", models.IntegerField(default=0, editable=False)),
                (
                    "completed_chapters",
                    models.ManyToManyField(blank=True, to="lessons.Chapter"),
                ),
                (
                    "last_submissions",
                    models.ManyToManyField(to="problems.ProblemSubmission"),
                ),
                (
                    "solved_exercices",
                    models.ManyToManyField(blank=True, to="lessons.Exercice"),
                ),
                (
                    "solved_problems",
                    models.ManyToManyField(blank=True, to="problems.Problem"),
                ),
                (
                    "student",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="progress",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
