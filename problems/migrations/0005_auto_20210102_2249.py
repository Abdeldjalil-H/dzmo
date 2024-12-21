from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("problems", "0004_auto_20210101_1832"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={"verbose_name": "تعليق", "verbose_name_plural": "التعليقات"},
        ),
        migrations.AlterModelOptions(
            name="problemsubmission",
            options={
                "verbose_name": "إجابة مسألة",
                "verbose_name_plural": "إجابات المسائل",
            },
        ),
        migrations.AddField(
            model_name="problemsubmission",
            name="correction_in_progress",
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
