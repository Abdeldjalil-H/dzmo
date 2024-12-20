from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("problems", "0009_auto_20210725_1327"),
    ]

    operations = [
        migrations.AddField(
            model_name="problem",
            name="level",
            field=models.IntegerField(
                choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
                default=1,
                verbose_name="المستوى",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="problem",
            name="source",
            field=models.CharField(blank=True, max_length=200, verbose_name="المصدر"),
        ),
        migrations.AddField(
            model_name="problem",
            name="statement",
            field=models.TextField(verbose_name="المسألة"),
            preserve_default=False,
        ),
    ]
