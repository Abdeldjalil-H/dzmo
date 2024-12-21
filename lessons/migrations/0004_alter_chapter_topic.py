from django.db import migrations

import lessons.models


class Migration(migrations.Migration):

    dependencies = [
        ("lessons", "0003_auto_20210102_2249"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chapter",
            name="topic",
            field=lessons.models.TopicField(
                choices=[
                    ("a", "جبر"),
                    ("g", "هندسة"),
                    ("nt", "نظرية الأعداد"),
                    ("c", "توفيقات"),
                    ("b", "أساسيات"),
                ],
                max_length=2,
                verbose_name="المادة",
            ),
        ),
    ]
