from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_auto_20210101_1831"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_corrector",
            field=models.BooleanField(default=False),
        ),
    ]
