import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("lessons", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Problem",
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
                ("statement", models.TextField(verbose_name="المسألة")),
                (
                    "level",
                    models.IntegerField(
                        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
                        verbose_name="المستوى",
                    ),
                ),
                (
                    "source",
                    models.CharField(blank=True, max_length=200, verbose_name="المصدر"),
                ),
                (
                    "solved_by",
                    models.IntegerField(
                        default=0, editable=False, verbose_name="عدد الحلول"
                    ),
                ),
                ("added_on", models.DateTimeField(auto_now_add=True)),
                ("publish", models.BooleanField(default=True)),
                (
                    "chapter",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="problems",
                        to="lessons.chapter",
                        verbose_name="المحور",
                    ),
                ),
            ],
            options={
                "verbose_name": "مسألة",
                "verbose_name_plural": "مسائل",
            },
        ),
        migrations.CreateModel(
            name="ProblemSubmission",
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
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "مسودة"),
                            ("submit", "تقديم الحل"),
                            ("wrong", "إجابة خاطئة"),
                            ("comment", "يوجد تعليق"),
                            ("correct", "إجابة صحيحة"),
                        ],
                        max_length=10,
                    ),
                ),
                ("correct", models.BooleanField(null=True)),
                ("solution", models.TextField()),
                ("submited_on", models.DateTimeField(auto_now=True)),
                ("file", models.FileField(blank=True, null=True, upload_to="")),
                (
                    "problem",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="problems.problem",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
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
                ("content", models.TextField(verbose_name="")),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "submission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="problems.problemsubmission",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
