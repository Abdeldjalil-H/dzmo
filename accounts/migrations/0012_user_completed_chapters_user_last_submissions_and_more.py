from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lessons", "0004_alter_chapter_topic"),
        ("problems", "0014_alter_comment_options_alter_problem_options_and_more"),
        ("tasks", "0006_remove_taskproblemsubmission_correct_alter_task_team"),
        ("accounts", "0011_remove_studentprogress_solved_problems"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="completed_chapters",
            field=models.ManyToManyField(
                blank=True, to="lessons.chapter", verbose_name="المحاور المتمة"
            ),
        ),
        migrations.RunSQL(
            sql="""
            INSERT INTO accounts_user_completed_chapters (id, user_id, chapter_id)
            SELECT cc.id, student_id user_id, chapter_id
            FROM accounts_studentprogress_completed_chapters cc 
            JOIN accounts_studentprogress sp ON cc.studentprogress_id = sp.id;
            """,
            reverse_sql="DELETE FROM accounts_user_completed_chapters;",
        ),
        migrations.AddField(
            model_name="user",
            name="last_submissions",
            field=models.ManyToManyField(
                blank=True,
                to="problems.problemsubmission",
                verbose_name="آخر المحاولات المقدمة",
            ),
        ),
        migrations.RunSQL(
            sql="""
            INSERT INTO accounts_user_last_submissions (id, user_id, problemsubmission_id)
            SELECT ls.id, student_id user_id, problemsubmission_id 
            FROM accounts_studentprogress_last_submissions ls 
            JOIN accounts_studentprogress sp ON ls.studentprogress_id = sp.id;
            """,
            reverse_sql="DELETE FROM accounts_user_last_submissions;",
        ),
        migrations.AddField(
            model_name="user",
            name="last_tasks_subs",
            field=models.ManyToManyField(blank=True, to="tasks.taskproblemsubmission"),
        ),
        migrations.RunSQL(
            sql="""
            INSERT INTO accounts_user_last_tasks_subs (id, user_id, taskproblemsubmission_id)
            SELECT lts.id, student_id user_id, taskproblemsubmission_id 
            FROM accounts_studentprogress_last_tasks_subs lts
            JOIN accounts_studentprogress sp ON lts.studentprogress_id = sp.id;
            """,
            reverse_sql="DELETE FROM accounts_user_last_tasks_subs;",
        ),
        migrations.AddField(
            model_name="user",
            name="points",
            field=models.IntegerField(db_index=True, default=0, editable=False),
        ),
        migrations.RunSQL(
            sql="UPDATE accounts_user SET points = sp.points FROM accounts_studentprogress sp WHERE accounts_user.id = sp.student_id;",
        ),
        migrations.AddField(
            model_name="user",
            name="solved_exercices",
            field=models.ManyToManyField(
                blank=True, to="lessons.exercice", verbose_name="التمارين المحلولة"
            ),
        ),
        migrations.RunSQL(
            sql="""
            INSERT INTO accounts_user_solved_exercices (id, user_id, exercice_id)
            SELECT se.id, student_id user_id, exercice_id 
            FROM accounts_studentprogress_solved_exercices se 
            JOIN accounts_studentprogress sp ON se.studentprogress_id = sp.id;
            """,
            reverse_sql="DELETE FROM accounts_user_solved_exercices;",
        ),
        migrations.DeleteModel(
            name="StudentProgress",
        ),
    ]
