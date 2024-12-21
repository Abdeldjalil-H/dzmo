from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tests", "0004_auto_20210120_0850"),
    ]

    operations = [
        migrations.AlterField(
            model_name="testanswer",
            name="mark",
            field=models.IntegerField(default=0),
        ),
    ]
