from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("problems", "0007_comment_ltr_dir"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="ltr_dir",
            field=models.BooleanField(default=False, verbose_name="الكتابة من اليسار"),
        ),
    ]
