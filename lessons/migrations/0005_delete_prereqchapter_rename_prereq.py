from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lessons", "0004_alter_chapter_topic"),
    ]

    operations = [
        migrations.RenameField(
            model_name="chapter",
            old_name="prereq",
            new_name="prerequisites",
        ),
        migrations.AlterField(
            model_name="chapter",
            name="prerequisites",
            field=models.ManyToManyField(
                blank=True, to="lessons.chapter", verbose_name="المكتسبات اللازمة"
            ),
        ),
        migrations.DeleteModel(name="PrereqChapter"),
    ]
