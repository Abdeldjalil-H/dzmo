from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=60, unique=True, verbose_name="البريد الإلكتروني"
                    ),
                ),
                ("first_name", models.CharField(max_length=25, verbose_name="الاسم")),
                ("last_name", models.CharField(max_length=25, verbose_name="اللقب")),
                (
                    "date_of_birth",
                    models.DateField(
                        blank=True, null=True, verbose_name="تاريخ الميلاد"
                    ),
                ),
                (
                    "grade",
                    models.IntegerField(
                        choices=[
                            (-3, "السنة 1 متوسط"),
                            (-2, "السنة 2 متوسط"),
                            (-1, "السنة 3 متوسط"),
                            (0, "السنة 4 متوسط"),
                            (1, "السنة 1 ثانوي"),
                            (2, "السنة 2 ثانوي"),
                            (3, "السنة 3 ثانوي"),
                            (4, "غير ذلك"),
                        ],
                        null=True,
                        verbose_name="العام الدراسي",
                    ),
                ),
                (
                    "sex",
                    models.CharField(
                        choices=[("m", "ذكر"), ("f", "أنثى")],
                        max_length=2,
                        verbose_name="الجنس",
                    ),
                ),
                (
                    "wilaya",
                    models.IntegerField(
                        choices=[
                            (1, 1),
                            (2, 2),
                            (3, 3),
                            (4, 4),
                            (5, 5),
                            (6, 6),
                            (7, 7),
                            (8, 8),
                            (9, 9),
                            (10, 10),
                            (11, 11),
                            (12, 12),
                            (13, 13),
                            (14, 14),
                            (15, 15),
                            (16, 16),
                            (17, 17),
                            (18, 18),
                            (19, 19),
                            (20, 20),
                            (21, 21),
                            (22, 22),
                            (23, 23),
                            (24, 24),
                            (25, 25),
                            (26, 26),
                            (27, 27),
                            (28, 28),
                            (29, 29),
                            (30, 30),
                            (31, 31),
                            (32, 32),
                            (33, 33),
                            (34, 34),
                            (35, 35),
                            (36, 36),
                            (37, 37),
                            (38, 38),
                            (39, 39),
                            (40, 40),
                            (41, 41),
                            (42, 42),
                            (43, 43),
                            (44, 44),
                            (45, 45),
                            (46, 46),
                            (47, 47),
                            (48, 48),
                        ],
                        null=True,
                        verbose_name="ولاية الإقامة",
                    ),
                ),
                (
                    "join_date",
                    models.DateField(auto_now_add=True, verbose_name="تاريخ الانضمام"),
                ),
                (
                    "username_abrv",
                    models.CharField(
                        choices=[
                            ("fl", "الاسم واللقب"),
                            ("f", "الاسم"),
                            ("l", "اللقب"),
                        ],
                        default="fl",
                        max_length=2,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_admin", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
