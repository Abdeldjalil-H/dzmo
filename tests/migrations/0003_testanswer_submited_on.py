from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tests", "0002_auto_20210118_1507"),
    ]

    operations = [
        migrations.AddField(
            model_name="testanswer",
            name="submited_on",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
