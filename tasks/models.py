import os
from django.utils import timezone
from accounts.models import Team
from django.conf import settings
from django.db import models
from django.shortcuts import get_object_or_404
from problems.models import ( 
    AbstractComment,
    AbstractPbSubmission, 
    Comment,
    AbstractProblem
)

class TaskProblem(AbstractProblem):
    def get_name(self):
        return f'Problem'
    def has_draft_sub(self, user):
        return self.submissions.filter(student=user, status='draft').exists()
    def get_user_subs(self, user):
        return self.submissions.filter(student=user, status__isnull=False)
    def get_all_subs(self):
        return self.submissions.all()
    def get_sub(self, **kwargs):
        return get_object_or_404(self.submissions, **kwargs)
    
    def has_submited(self, user):
        return self.submissions.filter(student=user).exists()
    
    def has_solved(self, user):
        return self.submissions.filter(student=user, correct=True).exists()
    def get_draft_sub(self, user):
        return self.submissions.filter(student=user).first()
        return self.submissions.filter(student=user, status='draft').first()
    def can_submit(self, user):
        #if draft or no sub
        sub = self.get_user_subs(user).first()
        return not sub or sub.status == 'draft'

    def get_code(self):
        return f'{self.pk}'

    class Meta:
        verbose_name = 'مسألة واجبات'
        verbose_name_plural = 'مسائل الواجبات'
        ordering = ['pk']

def file_path_name(instance, filename):
    ext = filename.split('.')[-1]
    name = f'{instance.problem.pk}_u{instance.student.pk}.{ext}'
    return os.path.join('tasks_subs',f'pb{instance.problem.pk}', name)
class TaskProblemSubmission(AbstractPbSubmission):
    student     = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete = models.CASCADE, related_name='tasks_submissions')
    problem     = models.ForeignKey(TaskProblem, on_delete = models.CASCADE, related_name='submissions')
    file        = models.FileField(blank = True, null = True, upload_to = file_path_name)

    def set_submited_now(self):
        self.submited_on = timezone.now()
    def update(self, solution, dir, status):
        self.solution=solution
        self.ltr_dir=dir
        self.status=status
        self.submited_on = timezone.now()
        self.save()
    def set_dir(self, dir):
        self.ltr_dir = dir
    class Meta:
        verbose_name = 'إجابة مسألة واجب'
        verbose_name_plural = 'إجابات مسائل الواجبات'
class Task(models.Model):
    name        = models.CharField(max_length=100, null=True)
    team        = models.ManyToManyField(Team, related_name='tasks')
    problems    = models.ManyToManyField(TaskProblem, blank=True)
    started_on  = models.DateField()
    ended_on    = models.DateField()

    def __str__(self):
        return f'الواجب {self.pk}'
    def get_name(self):
        if self.name:
            return self.name
        return ''

    def get_problems_by_level(self):
        return [self.problems.filter(level = k) for k in range(1,6)]

    def get_subs_by_level(self):
        all_subs = TaskProblemSubmission.objects.filter(problem__in = self.problems.all(), student__team__in = self.team.all(), status__in = ['submit','comment'])
        return [all_subs.filter(problem__level = k) for k in range(1,6)]
    def has_access(self, user):
        if user.is_staff:
            return True
        if not user.is_team_member():
            return False
        return user.team in self.team.all()
class TaskComment(AbstractComment):
        submission  = models.ForeignKey(TaskProblemSubmission,related_name = 'comments',on_delete= models.CASCADE)

        class Meta:
            ordering = ['date']
            verbose_name = 'تعليق واجب'
            verbose_name_plural = 'تعليقات الواجبات'