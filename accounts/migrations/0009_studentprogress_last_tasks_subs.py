from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0001_initial"),
        ("accounts", "0008_auto_20210809_1439"),
    ]

    operations = [
        migrations.AddField(
            model_name="studentprogress",
            name="last_tasks_subs",
            field=models.ManyToManyField(blank=True, to="tasks.TaskProblemSubmission"),
        ),
    ]
