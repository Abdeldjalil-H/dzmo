from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lessons", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exercice",
            name="image",
            field=models.ImageField(blank=True, upload_to="exercices_images"),
        ),
    ]
