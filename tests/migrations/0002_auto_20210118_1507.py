import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tests", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="test",
            options={"verbose_name": "إختبار", "verbose_name_plural": "إختبارات"},
        ),
        migrations.AlterModelOptions(
            name="testanswer",
            options={
                "verbose_name": "إجابة اختبار",
                "verbose_name_plural": "إجابات الإختبارات",
            },
        ),
        migrations.AddField(
            model_name="test",
            name="correction",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="testanswer",
            name="start_time",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="test",
            name="passed_by",
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
