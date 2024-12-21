from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("control", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="mainpagepost",
            name="public",
            field=models.BooleanField(default=True),
        ),
    ]
