from django.db import models
from django.core.mail import send_mail
from problems.models import ProblemSubmission
from django.conf import settings
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
    num_old_subs        = models.IntegerField(default = 0)
    num_corrected_subs  = models.IntegerField(default=0)
    notif_each          = models.IntegerField(default = 3)
    
    @property
    def total_subs(self):
        return ProblemSubmission.objects.filter(status__in = ['submit','comment']).count()

    def emails_list(self):
        pass
    def have_to_send_mail(self):
        if self.total_subs > self.num_old_subs and self.total_subs % self.notif_each ==0:
            #send_email
            res = send_mail(
                subject = 'إجابات جديدة',
                message = f'هناك {self.total_subs} إجابة لم يتم تصحيحها.',
                from_email = settings.DEFAULT_FROM_EMAIL,
                recipient_list = ['djaloulehez3@gmail.com','chen.anas@gmail.com'],
                fail_silently=False,
                )
            if res:
                self.num_old_subs       = self.total_subs
                self.num_corrected_subs = 0
                self.save()
