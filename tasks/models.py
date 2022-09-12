from os.path import join
from django.conf import settings
from django.db import models
from problems.models import (
    AbstractComment,
    AbstractPbSubmission,
    AbstractProblem,
)
from accounts.models import Team

TASKS_MAX_LEVEL = 6
TASKS_LEVELS = [(i, str(i)) for i in range(1, TASKS_MAX_LEVEL+1)]
class TaskProblem(AbstractProblem):

    level = models.IntegerField(
        choices=TASKS_LEVELS,
        verbose_name='المستوى',
    )

    def get_name(self):
        return f'Problem'

    @property
    def code(self):
        return f'{self.pk}'

    class Meta:
        verbose_name = 'مسألة واجبات'
        verbose_name_plural = 'مسائل الواجبات'
        ordering = ['pk']

    def __str__(self):
        return self.source if self.source else f'pb {self.pk}'

def file_path_name(instance, filename):
    ext = filename.split('.')[-1]
    name = f'{instance.problem.pk}_u{instance.student.pk}.{ext}'
    return join('tasks_subs', f'pb{instance.problem.pk}', name)


class TaskProblemSubmission(AbstractPbSubmission):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks_submissions',
    )
    problem = models.ForeignKey(
        TaskProblem,
        on_delete=models.CASCADE,
        related_name='submissions',
    )
    file = models.FileField(
        blank=True,
        null=True,
        upload_to=file_path_name,
    )

    def set_dir(self, dir):
        self.ltr_dir = dir

    def mark_as_seen(self, user):
        user.progress.last_tasks_subs.remove(self)

    def get_task(self):
        return self.problem.task.get(team=self.student.team)

    class Meta:
        verbose_name = 'إجابة مسألة واجب'
        verbose_name_plural = 'إجابات مسائل الواجبات'


class Task(models.Model):
    name = models.CharField(max_length=100, null=True)
    team = models.ManyToManyField(Team, related_name='tasks', null=True)
    problems = models.ManyToManyField(
        TaskProblem,
        related_name='task',
        blank=True,
    )
    started_on = models.DateField()
    ended_on = models.DateField()

    def __str__(self):
        return f'الواجب {self.pk}'

    def get_name(self):
        return self.name or ''

    def get_problems_by_level(self):
        return [self.problems.filter(level=k) for k in range(1, TASKS_MAX_LEVEL+1)]

    def get_subs_by_level(self):
        all_subs = TaskProblemSubmission.objects.filter(
            problem__in=self.problems.all(),
            student__team__in=self.team.all(),
            status__in=['submit', 'comment'])
        return [all_subs.filter(problem__level=k) for k in range(1, TASKS_MAX_LEVEL+1)]

    def get_correct_pks(self, user):
        return list(
            TaskProblemSubmission.objects.filter(
                problem__in=self.problems.all(), student=user,
                correct=True).values_list('problem__pk', flat=True))

    def get_wrong_pks(self, user):
        return list(
            TaskProblemSubmission.objects.filter(
                problem__in=self.problems.all(),
                student=user,
                correct=False,
            ).values_list(
                'problem__pk',
                flat=True,
            ))

    def get_pending_pks(self, user):
        return list(
            TaskProblemSubmission.objects.filter(
                problem__in=self.problems.all(),
                student=user,
                status='submit',
            ).values_list(
                'problem__pk',
                flat=True,
            ))

    def has_access(self, user):
        if user.is_staff:
            return True
        if not user.is_team_member():
            return False
        return user.team in self.team.all()

    class Meta:
        verbose_name = 'واجب'
        verbose_name_plural = 'واجبات'


class TaskComment(AbstractComment):
    submission = models.ForeignKey(
        TaskProblemSubmission,
        related_name='comments',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['date']
        verbose_name = 'تعليق واجب'
        verbose_name_plural = 'تعليقات الواجبات'
