from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tests", "0005_auto_20210120_1011"),
    ]

    operations = [
        migrations.AddField(
            model_name="testanswer",
            name="char_file",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="testanswer",
            name="answer_file",
            field=models.FileField(upload_to=""),
        ),
    ]
