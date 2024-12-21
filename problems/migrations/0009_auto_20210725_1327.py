from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("problems", "0008_auto_20210602_2231"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="problem",
            name="level",
        ),
        migrations.RemoveField(
            model_name="problem",
            name="source",
        ),
        migrations.RemoveField(
            model_name="problem",
            name="statement",
        ),
    ]
