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
    class Meta:
        verbose_name        = 'إختبار'
        verbose_name_plural = 'إختبارات'

class TestAnswer(models.Model):
    test        = models.ForeignKey(Test, on_delete = models.SET_NULL, null=True)
    student     = models.ForeignKey(User, on_delete = models.CASCADE)
    answer_file = models.FileField(upload_to = 'tests',)
    start_time  = models.DateTimeField(auto_now_add = True)
    submited_on = models.DateTimeField(blank = True, null = True)
    #corrector part
    mark        = models.IntegerField(null = True)
    comment     = models.TextField(blank = True, null = True)

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

    def can_answer(self,test):
        return self.remaining_time(test) and not self.answer_submited
    
    def add_ans_file(self, file):
        self.answer_file = file
        self.save()

    def submited_now(self):
        self.submited_on = timezone.now()
        self.save()
    class Meta:
        verbose_name        = 'إجابة اختبار'
        verbose_name_plural = 'إجابات الإختبارات'