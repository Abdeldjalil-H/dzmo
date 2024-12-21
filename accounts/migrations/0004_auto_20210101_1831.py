from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_auto_20201225_2253"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username_abrv",
            field=models.CharField(
                choices=[("fl", "الاسم واللقب"), ("f", "الاسم"), ("l", "اللقب")],
                default="fl",
                max_length=2,
                verbose_name="طريقة عرض الاسم",
            ),
        ),
    ]
