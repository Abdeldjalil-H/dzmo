from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="task",
            options={"verbose_name": "واجب", "verbose_name_plural": "واجبات"},
        ),
        migrations.AlterField(
            model_name="taskproblemsubmission",
            name="solution",
            field=models.TextField(blank=True, null=True),
        ),
    ]
