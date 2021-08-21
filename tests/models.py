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
    ltr         = models.BooleanField(default=True)
    number_of_pbs = models.PositiveSmallIntegerField(editable=False, default=1)
    def count_problems(self):
        return self.number_of_pbs

    def get_problems(self):
        return self.problems.all()
    
    def get_problems_order(self):
        return list(self.problems.values_list('pk', flat=True))
    
    def is_participant(self, user):
        return self.submissions.filter(student=user).exists()
    
    def get_participants(self):
        pass
        #return self.submissions.
    def get_submission(self, user):
        return self.submissions.filter(student=user).first()
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

def answer_file_path(instance, *args, pb_num=None):
    if not pb_num:
        pb_num = instance.pb_num
    #ext = filename.split('.')[-1]
    #name = f'{instance.pb_pk}.{ext}'
    return join(parent_file_path(instance), f'{pb_num}')

class TestAnswer(models.Model):
    test        = models.ForeignKey(Test, on_delete=models.SET_NULL, null=True, related_name='submissions')
    student     = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time  = models.DateTimeField(auto_now_add=True)
    submited_on = models.DateTimeField(blank=True, null=True)
    #corrector part
    mark        = models.IntegerField(default=0)
    comment     = models.TextField(blank=True, null=True)
    corrected   = models.BooleanField(default=False)
    
    files = models.FileField(upload_to=answer_file_path, blank=True, null=True)
    uploaded_files = models.CharField(max_length=15, blank=True, null=True)
    
    def delete(self):
        self.files.delete(save=False)
        super().delete()
    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.set_start_now()
        instance.uploaded_files = '0' * kwargs['test'].number_of_pbs
        return instance

    def set_file_uploaded(self, pb_num):
        number_of_pbs = self.test.number_of_pbs
        new = bin(int(self.uploaded_files, 2) | 1 << (number_of_pbs-pb_num))
        self.uploaded_files = new[2:].zfill(number_of_pbs)

    def get_files_status(self):
        return [int(x) for x in self.uploaded_files]
    def set_files_path(self):
        self.files = parent_file_path(self)
    

    def remaining_time(self, test):
        remains = self.start_time + test.duration - timezone.now()  
        if remains.days >= 0:
            return remains
        else:
            return 0

    @property
    def can_answer(self):
        return self.remaining_time(self.test)

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
    problem_number = models.PositiveSmallIntegerField(default=1)
    class Meta:
        ordering = ['problem_number']