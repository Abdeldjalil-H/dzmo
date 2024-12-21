from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tests", "0007_auto_20210126_2235"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="testanswer",
            name="char_file",
        ),
        migrations.AlterField(
            model_name="testanswer",
            name="answer_file",
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
