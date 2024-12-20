import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import problems.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("problems", "0010_auto_20210725_1335"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={
                "ordering": ["date"],
                "verbose_name": "تعليق",
                "verbose_name_plural": "التعليقات",
            },
        ),
        migrations.AlterModelOptions(
            name="problem",
            options={
                "ordering": ["added_on"],
                "verbose_name": "مسألة",
                "verbose_name_plural": "مسائل",
            },
        ),
        migrations.AlterModelOptions(
            name="problemsubmission",
            options={
                "ordering": ["submited_on"],
                "verbose_name": "إجابة مسألة",
                "verbose_name_plural": "إجابات المسائل",
            },
        ),
        migrations.RemoveField(
            model_name="problem",
            name="publish",
        ),
        migrations.RemoveField(
            model_name="problem",
            name="solved_by",
        ),
        migrations.AlterField(
            model_name="comment",
            name="content",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="problemsubmission",
            name="file",
            field=models.FileField(
                blank=True, null=True, upload_to=problems.models.file_name
            ),
        ),
        migrations.AlterField(
            model_name="problemsubmission",
            name="problem",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="submissions",
                to="problems.problem",
            ),
        ),
        migrations.AlterField(
            model_name="problemsubmission",
            name="status",
            field=models.CharField(
                choices=[
                    ("draft", "مسودة"),
                    ("submit", "تقديم الحل"),
                    ("wrong", "إجابة خاطئة"),
                    ("comment", "يوجد تعليق"),
                    ("correct", "إجابة صحيحة"),
                ],
                max_length=10,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="problemsubmission",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="submissions",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
