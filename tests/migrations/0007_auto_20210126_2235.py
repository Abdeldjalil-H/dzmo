from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tests", "0006_auto_20210126_2200"),
    ]

    operations = [
        migrations.AlterField(
            model_name="testanswer",
            name="char_file",
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
