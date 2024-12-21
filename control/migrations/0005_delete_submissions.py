from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("control", "0004_auto_20210818_1019"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Submissions",
        ),
    ]
