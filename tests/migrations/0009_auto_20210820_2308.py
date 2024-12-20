import django.db.models.deletion
from django.db import migrations, models

import tests.models


class Migration(migrations.Migration):

    dependencies = [
        ("tests", "0008_auto_20210126_2243"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="test",
            name="correction",
        ),
        migrations.RemoveField(
            model_name="test",
            name="passed_by",
        ),
        migrations.RemoveField(
            model_name="test",
            name="problems",
        ),
        migrations.RemoveField(
            model_name="test",
            name="total_score",
        ),
        migrations.RemoveField(
            model_name="testanswer",
            name="answer_file",
        ),
        migrations.AddField(
            model_name="test",
            name="ltr",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="test",
            name="number_of_pbs",
            field=models.PositiveSmallIntegerField(default=1, editable=False),
        ),
        migrations.AddField(
            model_name="testanswer",
            name="files",
            field=models.FileField(
                blank=True, null=True, upload_to=tests.models.answer_file_path
            ),
        ),
        migrations.AddField(
            model_name="testanswer",
            name="uploaded_files",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name="testanswer",
            name="test",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="submissions",
                to="tests.test",
            ),
        ),
        migrations.CreateModel(
            name="TestProblem",
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
                ("solution", models.TextField(blank=True, null=True)),
                ("problem_number", models.PositiveSmallIntegerField(default=1)),
                (
                    "test",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="problems",
                        to="tests.test",
                    ),
                ),
            ],
            options={
                "ordering": ["problem_number"],
            },
        ),
    ]
