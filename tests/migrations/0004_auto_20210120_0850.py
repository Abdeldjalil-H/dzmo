from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tests", "0003_testanswer_submited_on"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="test",
            options={"verbose_name": "اختبار", "verbose_name_plural": "اختبارات"},
        ),
        migrations.AlterModelOptions(
            name="testanswer",
            options={
                "verbose_name": "إجابة اختبار",
                "verbose_name_plural": "إجابات الاختبارات",
            },
        ),
        migrations.AddField(
            model_name="testanswer",
            name="corrected",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="testanswer",
            name="mark",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
