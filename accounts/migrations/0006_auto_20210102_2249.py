from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lessons", "0003_auto_20210102_2249"),
        ("problems", "0005_auto_20210102_2249"),
        ("accounts", "0005_user_is_corrector"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="studentprogress",
            options={
                "verbose_name": "تقدم التلميذ",
                "verbose_name_plural": "تقدم التلاميذ",
            },
        ),
        migrations.AlterModelOptions(
            name="user",
            options={"verbose_name": "مستخدم", "verbose_name_plural": "المستخدمون"},
        ),
        migrations.AlterField(
            model_name="studentprogress",
            name="completed_chapters",
            field=models.ManyToManyField(
                blank=True, to="lessons.Chapter", verbose_name="المحاور المتمة"
            ),
        ),
        migrations.AlterField(
            model_name="studentprogress",
            name="last_submissions",
            field=models.ManyToManyField(
                blank=True,
                to="problems.ProblemSubmission",
                verbose_name="آخر المحاولات المقدمة",
            ),
        ),
        migrations.AlterField(
            model_name="studentprogress",
            name="solved_exercices",
            field=models.ManyToManyField(
                blank=True, to="lessons.Exercice", verbose_name="التمارين المحلولة"
            ),
        ),
        migrations.AlterField(
            model_name="studentprogress",
            name="solved_problems",
            field=models.ManyToManyField(
                blank=True, to="problems.Problem", verbose_name="المسائل المحلولة"
            ),
        ),
    ]
