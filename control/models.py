from problems.models import ProblemSubmission
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from requests import post
from django.utils import timezone
from datetime import timedelta
from json import dumps
# Create your models here.

class MainPagePost(models.Model):
    title           = models.CharField(max_length = 200, verbose_name='العنوان')
    content         = models.TextField(verbose_name='المحتوى')
    publish         = models.BooleanField(default=False)
    publish_date    = models.DateTimeField(auto_now_add = True)
    image           = models.ImageField(blank = True, null= True,
                                        verbose_name='صورة')
    public          = models.BooleanField(default = True)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name        = 'منشور الصفحة الرئيسية'
        verbose_name_plural = 'منشورات الصفحة الرئيسية'

class CorrectorsNotif(models.Model):
    new_subs    = models.SmallIntegerField(default=0)
    notif_each  = models.SmallIntegerField(default=5)
    url         = models.URLField(blank=True, null=True)
    
    def notify(self):
        msg = f'''هناك {Submissions.count_subs()} إجابة جديدة.
        '''
        data = dumps({
            'username': 'Grader Notif',
            'content': msg,
        })

        post(self.url, data=data, headers = {'Content-Type': 'application/json'}) 
        
    def update(self, status):
        if status in ['submit','comment']:
            if self.new_subs == self.notif_each - 1:
                self.new_subs = 0
                self.notify()
            else:
                self.new_subs += 1
        elif status != 'draft' and self.new_subs > 0:
            self.new_subs -= 1
        self.save()

class Submissions(models.Model):
    problems_subs = models.ManyToManyField(ProblemSubmission, blank=True, related_name='+')
    last_correct_subs = models.ManyToManyField(ProblemSubmission, blank=True, related_name='+')
    tasks_subs      = models.ManyToManyField('tasks.TaskProblemSubmission', blank=True, related_name='+')

    @classmethod
    def add_sub(cls, sub):
        return cls.objects.first().problems_subs.add(sub)
    
    @classmethod
    def remove_sub(cls, sub):
        cls.objects.first().problems_subs.remove(sub)
    @classmethod
    def add_correct_sub(cls, sub):
        return cls.objects.first().last_correct_subs.add(sub)
    
    @classmethod
    def count_subs(cls):
        return cls.objects.first().problems_subs.count()
    
    @classmethod
    def count_correct_subs(cls):
        return cls.objects.first().last_correct_subs.count()
    
    @classmethod
    def get_problems_subs(cls, **kwargs):
        return cls.objects.first().problems_subs.filter(**kwargs)
    @classmethod
    def get_problems_subs_by_level(cls, **kwargs):
        subs = cls.objects.first().problems_subs.all()
        return [subs.filter(problem__level = k) for k in range(1,6)]
    
    @classmethod
    def remove_correct_subs(cls, *args):
        cls.objects.first().last_correct_subs.remove(*args)
    
    @classmethod
    def update_last_correct(cls):
        cls.remove_correct_subs(*cls.objects.first().last_correct_subs.filter(submited_on__lt = timezone.now()-timedelta(days=7)))
    @classmethod
    def get_last_correct(cls, **kwargs):
        return cls.objects.first().last_correct_subs.filter(**kwargs)

def init_submissions():
    if Submissions.objects.first():
        instance = Submissions.objects.first() 
    else:
        instance = Submissions()
        instance.save()
    instance.problems_subs.add(*ProblemSubmission.objects.filter(status__in = ['submit', 'comment']))
    instance.last_correct_subs.add(*ProblemSubmission.objects.filter(submited_on__gte = timezone.now()-timedelta(days=7)))