from django.db import models
from django.conf import settings
from lessons.models import Chapter


LEVELS = [(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')]

class Problem(models.Model):
    statement   = models.TextField(verbose_name ='المسألة')
    level       = models.IntegerField(choices = LEVELS,
                                      verbose_name = 'المستوى')
    chapter     = models.ForeignKey(Chapter, related_name = 'problems',
                                    on_delete = models.SET_NULL,
                                    null = True,
                                    verbose_name = 'المحور'
                                    )
    source      = models.CharField(max_length = 200, blank = True,
                                    verbose_name = 'المصدر')
    solved_by   = models.IntegerField(  default = 0, editable = False,
                                        verbose_name = 'عدد الحلول')
    added_on    = models.DateTimeField(auto_now_add = True)
    #we use False for tests
    publish     = models.BooleanField(default = True)

    def has_access(self, request):
        return self.chapter in request.user.progress.completed_chapters.all()

    @property
    def points(self):
        return 15*self.level
    
    def __str__(self):
        return f'مسألة {self.id}. {self.chapter.name}'
    class Meta:
        verbose_name        = 'مسألة'
        verbose_name_plural = 'مسائل'

STATUS = [
    ('draft', 'مسودة'),
    ('submit', 'تقديم الحل'),
    ('wrong', 'إجابة خاطئة'),
    ('comment', 'يوجد تعليق'),
    ('correct', 'إجابة صحيحة')
]
class ProblemSubmission(models.Model):
    ''' 
    the status 'draft', 'submit', 'correct', 'wrong', 'comment'
    will appear to others iff correct
    will appear to the correcter if: submit or comment
    student take notif if wrong or correct
    '''
    status      = models.CharField(max_length = 10, 
                                   choices = STATUS)
    correct     = models.BooleanField(null = True)
    solution    = models.TextField()
    submited_on = models.DateTimeField(blank = True, null = True)
    problem     = models.ForeignKey(Problem,
                                    on_delete = models.CASCADE)
    student     = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete = models.CASCADE)
    file        = models.FileField(blank = True, null = True,
                                    upload_to = 'students_subs'
                                    )
    correction_in_progress = models.BooleanField(default = False, editable = False) 
    def __str__(self):
        return 'submission ' +str(self.id)

    class Meta:
        verbose_name        = 'إجابة مسألة'
        verbose_name_plural = 'إجابات المسائل'

class Comment(models.Model):
    content     = models.TextField('')
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.SET_NULL, null = True)
    date        = models.DateTimeField(auto_now_add = True)
    submission  = models.ForeignKey(ProblemSubmission,
                                    related_name = 'comments',
                                    on_delete= models.CASCADE)

    class Meta:
        verbose_name        = 'تعليق'
        verbose_name_plural = 'التعليقات'