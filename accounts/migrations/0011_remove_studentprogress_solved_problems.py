from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0010_corrector"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="studentprogress",
            name="solved_problems",
        ),
    ]
