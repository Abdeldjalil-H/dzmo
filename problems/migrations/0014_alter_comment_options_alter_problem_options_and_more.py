from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("problems", "0013_alter_comment_user"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={
                "ordering": ("date",),
                "verbose_name": "تعليق",
                "verbose_name_plural": "التعليقات",
            },
        ),
        migrations.AlterModelOptions(
            name="problem",
            options={
                "ordering": ("added_on",),
                "verbose_name": "مسألة",
                "verbose_name_plural": "مسائل",
            },
        ),
        migrations.AlterModelOptions(
            name="problemsubmission",
            options={
                "ordering": ("submited_on",),
                "verbose_name": "إجابة مسألة",
                "verbose_name_plural": "إجابات المسائل",
            },
        ),
        migrations.RemoveField(
            model_name="problemsubmission",
            name="correct",
        ),
    ]
