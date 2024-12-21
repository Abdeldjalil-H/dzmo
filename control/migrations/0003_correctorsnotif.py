from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("control", "0002_mainpagepost_public"),
    ]

    operations = [
        migrations.CreateModel(
            name="CorrectorsNotif",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("num_old_subs", models.IntegerField(default=0)),
                ("num_corrected_subs", models.IntegerField(default=0)),
                ("notif_each", models.IntegerField(default=3)),
            ],
        ),
    ]
