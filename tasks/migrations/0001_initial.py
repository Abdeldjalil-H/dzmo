# Generated by Django 3.1.3 on 2021-08-03 22:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tasks.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0007_auto_20210803_2345'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskProblem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statement', models.TextField(verbose_name='المسألة')),
                ('level', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name='المستوى')),
                ('source', models.CharField(blank=True, max_length=200, verbose_name='المصدر')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaskProblemSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('draft', 'مسودة'), ('submit', 'تقديم الحل'), ('wrong', 'إجابة خاطئة'), ('comment', 'يوجد تعليق'), ('correct', 'إجابة صحيحة')], max_length=10, null=True)),
                ('correct', models.BooleanField(null=True)),
                ('solution', models.TextField()),
                ('submited_on', models.DateTimeField(blank=True, null=True)),
                ('correction_in_progress', models.BooleanField(default=False, editable=False)),
                ('ltr_dir', models.BooleanField(default=False)),
                ('file', models.FileField(blank=True, null=True, upload_to=tasks.models.file_path_name)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='tasks.taskproblem')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks_submissions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaskComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('ltr_dir', models.BooleanField(default=False, verbose_name='الكتابة من اليسار')),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='tasks.taskproblemsubmission')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('started_on', models.DateField()),
                ('ended_on', models.DateField()),
                ('problems', models.ManyToManyField(to='tasks.TaskProblem')),
                ('team', models.ManyToManyField(related_name='tasks', to='accounts.Team')),
            ],
        ),
    ]