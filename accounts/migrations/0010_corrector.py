import django.contrib.postgres.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import accounts.models
import lessons.models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0009_studentprogress_last_tasks_subs"),
    ]

    operations = [
        migrations.CreateModel(
            name="Corrector",
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
                ("problems", models.BooleanField(default=True)),
                ("tasks", models.BooleanField(default=False)),
                ("tests", models.BooleanField(default=False)),
                ("self_correction", models.BooleanField(default=False)),
                ("solved_only", models.BooleanField(default=False)),
                (
                    "topics",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=lessons.models.TopicField(
                            choices=[
                                ("a", "جبر"),
                                ("g", "هندسة"),
                                ("nt", "نظرية الأعداد"),
                                ("c", "توفيقات"),
                                ("b", "أساسيات"),
                            ],
                            max_length=2,
                        ),
                        blank=True,
                        default=accounts.models.default_topics,
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
