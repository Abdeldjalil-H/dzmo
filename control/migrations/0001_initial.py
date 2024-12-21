from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MainPagePost",
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
                ("title", models.CharField(max_length=200, verbose_name="العنوان")),
                ("content", models.TextField(verbose_name="المحتوى")),
                ("publish", models.BooleanField(default=False)),
                ("publish_date", models.DateTimeField(auto_now_add=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="", verbose_name="صورة"
                    ),
                ),
            ],
            options={
                "verbose_name": "منشور الصفحة الرئيسية",
                "verbose_name_plural": "منشورات الصفحة الرئيسية",
            },
        ),
    ]
