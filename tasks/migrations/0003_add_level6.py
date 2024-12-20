from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0002_auto_20210815_1116"),
    ]

    operations = [
        migrations.AlterField(
            model_name="taskproblem",
            name="level",
            field=models.IntegerField(
                choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"), (6, "6")],
                verbose_name="المستوى",
            ),
        ),
    ]
