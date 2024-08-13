from problems.models import ProblemSubmission
from django.db import models
from requests import post
from json import dumps

# Create your models here.


class MainPagePost(models.Model):
    title = models.CharField(max_length=200, verbose_name="العنوان")
    content = models.TextField(verbose_name="المحتوى")
    publish = models.BooleanField(default=False)
    publish_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True, null=True, verbose_name="صورة")
    public = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "منشور الصفحة الرئيسية"
        verbose_name_plural = "منشورات الصفحة الرئيسية"


class CorrectorsNotif(models.Model):
    new_subs = models.SmallIntegerField(default=0)
    notif_each = models.SmallIntegerField(default=5)
    url = models.URLField(blank=True, null=True)

    def notify(self):
        msg = f"""هناك {ProblemSubmission.pending.count()} إجابة جديدة.
        """
        data = dumps(
            {
                "username": "Grader Notif",
                "content": msg,
            }
        )

        post(self.url, data=data, headers={"Content-Type": "application/json"})

    def update(self, status):
        if status in ["submit", "comment"]:
            if self.new_subs == self.notif_each - 1:
                self.new_subs = 0
                self.notify()
            else:
                self.new_subs += 1
        elif status != "draft" and self.new_subs > 0:
            self.new_subs -= 1
        self.save()
