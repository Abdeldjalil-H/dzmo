from django.db import models

# Create your models here.

class MainPagePost(models.Model):
    title           = models.CharField(max_length = 200, verbose_name='العنوان')
    content         = models.TextField(verbose_name='المحتوى')
    publish         = models.BooleanField(default=False)
    publish_date    = models.DateTimeField(auto_now_add = True)
    image           = models.ImageField(blank = True, null= True,
                                        verbose_name='صورة')
    def __str__(self):
        return self.title
    class Meta:
        verbose_name        = 'منشور الصفحة الرئيسية'
        verbose_name_plural = 'منشورات الصفحة الرئيسية'
