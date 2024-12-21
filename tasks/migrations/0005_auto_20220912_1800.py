from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0010_corrector"),
        ("tasks", "0004_auto_20220912_1331"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="team",
        ),
        migrations.AddField(
            model_name="task",
            name="team",
            field=models.ManyToManyField(
                null=True, related_name="tasks", to="accounts.Team"
            ),
        ),
    ]
