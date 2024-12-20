from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0011_remove_studentprogress_solved_problems"),
        ("tasks", "0005_auto_20220912_1800"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="taskproblemsubmission",
            name="correct",
        ),
        migrations.AlterField(
            model_name="task",
            name="team",
            field=models.ManyToManyField(related_name="tasks", to="accounts.team"),
        ),
    ]
