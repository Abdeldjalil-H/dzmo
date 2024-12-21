from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("problems", "0011_auto_20210803_2345"),
    ]

    operations = [
        migrations.AlterField(
            model_name="problemsubmission",
            name="solution",
            field=models.TextField(blank=True, null=True),
        ),
    ]
