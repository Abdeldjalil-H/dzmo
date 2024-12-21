from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_auto_20210102_2249"),
    ]

    operations = [
        migrations.CreateModel(
            name="Team",
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
                (
                    "color",
                    models.CharField(
                        choices=[
                            ("white", "white"),
                            ("green", "green"),
                            ("red", "red"),
                            ("black", "black"),
                        ],
                        max_length=100,
                        unique=True,
                    ),
                ),
            ],
        ),
    ]
