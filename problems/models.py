from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.conf import settings
from lessons.models import Chapter
from os.path import join

LEVELS = [(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')]
                             
class AbstractProblem(models.Model):
    statement   = models.TextField(verbose_name='المسألة')
    level       = models.IntegerField(choices=LEVELS,verbose_name='المستوى')
    source      = models.CharField(max_length=200, blank=True, verbose_name='المصدر')

    def has_draft_sub(self, user):
        return self.submissions.filter(student=user, status='draft').exists()

    def get_user_subs(self, user):
        return self.submissions.filter(student=user, status__isnull=False).exclude(status='draft')

    def has_submited(self, user):
        return self.submissions.filter(student=user).exists()

    def has_solved(self, user):
        return self.submissions.filter(student=user, correct=True).exists()

    def can_submit(self, user):
        #if draft or no sub
        sub = self.get_user_subs(user).first()
        return not sub or sub.status == 'draft'
    
    def get_correct_subs(self):
        return self.submissions.filter(correct=True)

    def get_sub(self, **kwargs):
        return get_object_or_404(self.submissions, **kwargs)

    def get_unique_sub(self, user):
        return self.submissions.filter(student=user).first()
    class Meta:
        abstract = True
    @property
    def points(self):
        return 15*self.level
class Problem(AbstractProblem):
    chapter     = models.ForeignKey(Chapter, related_name='problems', on_delete=models.SET_NULL, null=True, verbose_name='المحور')
    added_on    = models.DateTimeField(auto_now_add = True)

    def has_access(self, user):
        return self.chapter in user.progress.completed_chapters.all()
    def has_solved(self, user):
        return user.progress.solved_problems.filter(pk = self.pk).exists()
    def get_code(self):
        return f'{self.chapter.topic} {self.pk}'

    def get_topic(self):
        return self.chapter.get_topic()
    
    def get_name(self):
        return f'مسألة {self.get_topic()} مستوى {self.level}'
    def __str__(self):
        if self.chapter:
            return f'مسألة {self.id}. {self.chapter.name}'
        return f'مسألة {self.id} (محور محذوف)'
    class Meta:
        ordering = ['added_on']
        verbose_name        = 'مسألة'
        verbose_name_plural = 'مسائل'

STATUS = [
    ('draft', 'مسودة'),
    ('submit', 'تقديم الحل'),
    ('wrong', 'إجابة خاطئة'),
    ('comment', 'يوجد تعليق'),
    ('correct', 'إجابة صحيحة')
]
class AbstractPbSubmission(models.Model):
    status      = models.CharField(max_length = 10, choices = STATUS, null=True)
    correct     = models.BooleanField(null = True)
    solution    = models.TextField(blank=True, null=True)
    submited_on = models.DateTimeField(blank = True, null = True)
    correction_in_progress = models.BooleanField(default = False, editable = False) 
    ltr_dir     = models.BooleanField(default = False)

    def set_dir(self, dir):
        if dir:
            if dir == 'left':
                self.ltr_dir = True
            else:
                self.ltr_dir = False

    @property
    def get_dir_style(self):
        if self.ltr_dir:
            return 'dir=ltr style=text-align:left;'
        else:
            return 'dir=rtl style=text-align:right;'

    def get_dir_attrs(self):
        if self.ltr_dir:
            return {'dir':'ltr', 'style':'text-align:left;'}
        else:
            return {'dir':'rtl', 'style':'text-align:right;'}

    def set_status(self, status):
        self.status = status
    def set_student(self, user):
        self.student = user
    def set_solution(self, sol):
        self.solution = sol
    def get_comments(self):
        return self.comments.all()

    def can_be_corrected(self):
        return not self.correction_in_progress
    def set_correcting(self, in_progress):
        self.correction_in_progress = in_progress

    def set_submited_now(self):
        self.submited_on = timezone.now()
    def update(self, solution, dir, status, file):
        self.solution=solution
        self.ltr_dir=dir
        self.status=status
        self.file=file
        self.submited_on = timezone.now()
        self.save()
    
    def delete(self):
        # self.file.delete(save=False)
        super().delete()

    def soft_delete(self):
        # self.file.delete(save=False)
        Comment.objects.filter(submission=self).delete()
        self.solution=''
        self.submited_on=self.correct=self.status= None 
        self.correction_in_progress = False
        self.save()

    def can_be_deleted(self, user):
        return user == self.student and not self.correct and self.status == 'wrong'
    
    def can_comment(self, user):
        return user == self.student and self.status == 'wrong'

    def get_time_since_submit(self):
        return timezone.now() - self.submited_on
    def __str__(self):
        return f'إجابة {self.pk}: مسألة {self.problem.pk} {self.student.get_full_name()}'
    class Meta:
        abstract = True

def file_name(instance, filename):
    ext = filename.split('.')[-1]
    name = f'pb{instance.problem.pk}_u{instance.student.pk}.{ext}'
    return join('students_subs', f'pb{instance.problem.pk}', name)

class ProblemSubmission(AbstractPbSubmission):
    ''' 
    the status 'draft', 'submit', 'correct', 'wrong', 'comment'
    will appear to others iff correct
    will appear to the correcter if: submit or comment
    student take notif if wrong or correct
    '''
    problem     = models.ForeignKey(Problem, on_delete = models.CASCADE, related_name='submissions')
    student     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name='submissions')
    file        = models.FileField(blank = True, null = True, upload_to = file_name)
    def mark_as_seen(self, user):
        user.progress.last_submissions.remove(self)
    def __str__(self):
        return 'submission ' + str(self.id)

    class Meta:
        ordering = ['submited_on']
        verbose_name        = 'إجابة مسألة'
        verbose_name_plural = 'إجابات المسائل'

class AbstractComment(models.Model):
    content     = models.TextField()
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.SET_NULL, null = True)
    date        = models.DateTimeField(auto_now_add = True)
    ltr_dir     = models.BooleanField(default=False, 
    verbose_name='الكتابة من اليسار')
    @property
    def get_dir_style(self):
        if self.ltr_dir:
            return 'dir=ltr style=text-align:left;'
        else:
            return 'dir=rtl style=text-align:right;'
    def set_sub(self, sub):
        self.submission_id = sub.pk

    def set_user(self, user):
        self.user = user
    class Meta:
        abstract = True
class Comment(AbstractComment):
    submission  = models.ForeignKey(ProblemSubmission,related_name = 'comments', on_delete= models.CASCADE)

    class Meta:
        ordering = ['date']
        verbose_name        = 'تعليق'
        verbose_name_plural = 'التعليقات'