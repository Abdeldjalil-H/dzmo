from django.db import models
from django.utils import timezone
from accounts.models import User

class Test(models.Model):
    problems    = models.TextField()
    starts_at   = models.DateTimeField()
    ends_at     = models.DateTimeField(blank = True, null = True)
    duration    = models.DurationField()
    passed_by   = models.ManyToManyField(User, blank = True)
    total_score = models.IntegerField()
    long_time   = models.BooleanField(default = False)

    correction  = models.TextField(blank = True, null = True)

    @property
    def started(self):
        return timezone.now() >= self.starts_at
    @property
    def ends(self):
        return timezone.now() > self.ends_at
    @property
    def available(self):
        return self.started and not self.ends

    def __str__(self):
        return f'الاختبار {self.pk}'
    class Meta:
        verbose_name        = 'اختبار'
        verbose_name_plural = 'اختبارات'

class TestAnswer(models.Model):
    test        = models.ForeignKey(Test, on_delete = models.SET_NULL, null=True)
    student     = models.ForeignKey(User, on_delete = models.CASCADE)
    answer_file   = models.URLField(max_length=500, null = True, blank = True) 
    start_time  = models.DateTimeField(auto_now_add = True)
    submited_on = models.DateTimeField(blank = True, null = True)
    #corrector part
    mark        = models.IntegerField(default = 0)
    comment     = models.TextField(blank = True, null = True)
    corrected   = models.BooleanField(default = False)
    
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
        self.answer_file.url = 'https://drive.google.com/uc?export=view&id=' + file
        self.save()

    def submited_now(self):
        self.submited_on = timezone.now()
        self.save()

    def set_mark(self, mark, comment=''):
        self.mark = mark
        self.comment = comment
        self.save()
    def save(self, *args, **kwargs):
        if self.pk:
            old_mark = TestAnswer.objects.get(pk = self.pk).mark
            if self.mark - old_mark:
                self.student.progress.add_points(
                    self.mark - old_mark
                    )
        super().save(*args, **kwargs)
    def __str__(self):
        return f'إجابة الاختبار {self.test}: {self.student.username}'
    class Meta:
        verbose_name        = 'إجابة اختبار'
        verbose_name_plural = 'إجابات الاختبارات'