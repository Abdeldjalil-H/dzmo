from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("lessons", "0002_auto_20210101_1831"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="exercicesolution",
            options={
                "verbose_name": "إجابة التمرين",
                "verbose_name_plural": "إجابات التمارين",
            },
        ),
    ]
