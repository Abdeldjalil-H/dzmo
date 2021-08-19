from django.db import models
from django.utils import timezone
from accounts.models import User
from problems.models import AbstractProblem
from os.path import join

class Test(models.Model):
    starts_at   = models.DateTimeField()
    ends_at     = models.DateTimeField(blank=True, null=True)
    duration    = models.DurationField()
    long_time   = models.BooleanField(default=False)

    def count_problems(self):
        return self.problems.count()

    def get_problems(self):
        return self.problems.all()
    
    def is_participant(self, user):
        return self.submissions.filter(student=user).exists()
    
    def get_participants(self):
        pass
        #return self.submissions.
    
    @property
    def started(self):
        return timezone.now() >= self.starts_at
    
    @property
    def is_over(self):
        return timezone.now() > self.ends_at
    
    @property
    def is_available(self):
        return self.started and not self.ends

    def is_available_for(self, user):
        return self.is_over or self.is_participant(user)
    
    def __str__(self):
        return f'الاختبار {self.pk}'
    
    class Meta:
        verbose_name        = 'اختبار'
        verbose_name_plural = 'اختبارات'

def parent_file_path(instance):
    return join('tests', f'test{instance.test.pk}', f'student{instance.student.pk}')

def answer_file_path(instance, filename):
    ext = filename.split('.')[-1]
    name = f'{instance.pb_pk}.{ext}'
    return join(parent_file_path, name)

class TestAnswer(models.Model):
    test        = models.ForeignKey(Test, on_delete=models.SET_NULL, null=True, related_name='submissions')
    student     = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_file = models.URLField(max_length=500, null=True, blank=True) 
    start_time  = models.DateTimeField(auto_now_add=True)
    submited_on = models.DateTimeField(blank=True, null=True)
    #corrector part
    mark        = models.IntegerField(default=0)
    comment     = models.TextField(blank=True, null=True)
    corrected   = models.BooleanField(default=False)
    
    files = models.FileField(upload_to=answer_file_path, blank=True, null=True)
    
    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.set_start_now()
        instance.save()
    def set_files_path(self):
        self.files = parent_file_path()
    
    @property
    def answer_submited(self):
        if self.answer_file:
            return True
        return False

    def remaining_time(self, test):
        remains = self.start_time + test.duration - timezone.now()  
        if remains.days >= 0:
            return remains
        else:
            return 0

    @property
    def can_answer(self):
        return self.remaining_time(self.test) and not self.answer_submited
    
    def add_ans_file(self, file):
        self.answer_file = 'https://drive.google.com/uc?export=view&id=' + file
        self.save()

    def set_submited_now(self):
        self.submited_on = timezone.now()

    def set_start_now(self):
        self.start_time = timezone.now()
    
    def set_mark(self, mark, comment=''):
        self.mark = mark
        self.comment = comment

    def save(self, *args, **kwargs):
        if self.pk:
            old_mark = TestAnswer.objects.get(pk = self.pk).mark
            if self.mark - old_mark:
                self.student.progress.add_points(self.mark - old_mark)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'إجابة الاختبار {self.test}: {self.student.username}'
    
    class Meta:
        verbose_name        = 'إجابة اختبار'
        verbose_name_plural = 'إجابات الاختبارات'

class TestProblem(AbstractProblem):
    test        = models.ForeignKey(Test, related_name='problems', null=True, on_delete=models.SET_NULL)
    solution    = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['pk']