import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Chapter",
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
                ("name", models.CharField(max_length=150, verbose_name="عنوان المحور")),
                ("slug", models.SlugField(verbose_name="الرابط")),
                (
                    "topic",
                    models.CharField(
                        choices=[
                            ("a", "جبر"),
                            ("g", "هندسة"),
                            ("nt", "نظرية الأعداد"),
                            ("c", "توفيقات"),
                            ("b", "أساسيات"),
                        ],
                        max_length=20,
                        verbose_name="المادة",
                    ),
                ),
                ("descr", models.TextField(verbose_name="لمحة عن المحور")),
                (
                    "publish",
                    models.BooleanField(default=False, verbose_name="نشر المحور"),
                ),
                (
                    "pub_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="تاريخ النشر"),
                ),
            ],
            options={
                "verbose_name": "محور",
                "verbose_name_plural": "محاور",
            },
        ),
        migrations.CreateModel(
            name="Exercice",
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
                ("content", models.TextField(verbose_name="نص التمرين")),
                ("choices", models.TextField(blank=True, verbose_name="الاقتراحات")),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("one", "إختيار إجابة واحدة"),
                            ("multiple", "إختيار إجابات"),
                            ("result", "الإجابة بعدد"),
                        ],
                        max_length=30,
                        verbose_name="نوع التمرين",
                    ),
                ),
                ("solution", models.CharField(max_length=20, verbose_name="الإجابة")),
                ("explanation", models.TextField(blank=True, verbose_name="شرح الحل")),
                ("image", models.ImageField(blank=True, upload_to="")),
                (
                    "points",
                    models.IntegerField(
                        choices=[(3, "3"), (6, "6"), (9, "9"), (12, "12")], default=3
                    ),
                ),
                (
                    "chapter",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="lessons.chapter",
                        verbose_name="المحور",
                    ),
                ),
            ],
            options={
                "verbose_name": "تمرين",
                "verbose_name_plural": "تمارين",
            },
        ),
        migrations.CreateModel(
            name="PrereqChapter",
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
                ("name", models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name="Lesson",
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
                ("title", models.CharField(max_length=150, verbose_name="العنوان")),
                ("slug", models.SlugField(verbose_name="الرابط")),
                ("content", models.TextField(verbose_name="محتوى الدرس")),
                ("video", models.URLField(blank=True, verbose_name="رابط فيديو")),
                ("links", models.TextField(blank=True, verbose_name="روابط مفيدة")),
                (
                    "order",
                    models.PositiveIntegerField(
                        default=1, verbose_name="ترتيب الدرس في المحور"
                    ),
                ),
                (
                    "chapter",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="lessons.chapter",
                        verbose_name="المحور",
                    ),
                ),
            ],
            options={
                "verbose_name": "درس",
                "verbose_name_plural": "دروس",
            },
        ),
        migrations.CreateModel(
            name="ExerciceSolution",
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
                ("correct", models.BooleanField(default=False)),
                ("answer", models.CharField(max_length=30)),
                ("num_of_tries", models.IntegerField(default=0)),
                (
                    "exercice",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="lessons.exercice",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="chapter",
            name="prereq",
            field=models.ManyToManyField(
                blank=True, to="lessons.PrereqChapter", verbose_name="المكتسبات اللازمة"
            ),
        ),
    ]
