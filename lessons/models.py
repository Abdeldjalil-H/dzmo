from django.db import models
from django.conf import settings


class PrereqChapter(models.Model):
    name            = models.CharField( max_length = 150)
    def __str__(self):
        return self.name


TOPICS = [
	('a', 'جبر'),
	('g', 'هندسة'),
	('nt', 'نظرية الأعداد'),
	('c', 'توفيقات'),
	('b','أساسيات')
]

class Chapter(models.Model):
    name    = models.CharField( max_length = 150, 
                                verbose_name = 'عنوان المحور')
    slug    = models.SlugField(verbose_name='الرابط')
    topic   = models.CharField( max_length = 20, choices = TOPICS, 
                                verbose_name ='المادة')
    descr   = models.TextField(verbose_name = 'لمحة عن المحور')
    prereq  = models.ManyToManyField(PrereqChapter, blank = True, 
                                    verbose_name = 'المكتسبات اللازمة')
    publish = models.BooleanField(  default = False, 
                                    verbose_name = 'نشر المحور')
    pub_date= models.DateTimeField( auto_now_add = True, 
                                    verbose_name ='تاريخ النشر')

    @property
    def prereq_chapters(self):
        return Chapter.objects.filter(id__in = [ch.pk for ch in self.prereq.all()])
    
    def has_access(self, request):
        for ch in self.prereq.all(): 
            if Chapter.objects.get(id =ch.id) not in request.user.progress.completed_chapters.all():
                return False
        return True

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        print(self.id)
        if not self.id:
            ch = PrereqChapter(name=self.name ,id = self.id)  
        else:
            ch = PrereqChapter.objects.get(id = self.id)
            ch.name = self.name
        ch.save()
        return super().save(**kwargs)
    class Meta: 
        verbose_name        = 'محور'
        verbose_name_plural = 'محاور'



class Lesson(models.Model):
    title 	    = models.CharField(max_length = 150 , verbose_name ='العنوان')
    slug        = models.SlugField(verbose_name ='الرابط')
    content     = models.TextField(verbose_name ='محتوى الدرس')
    chapter     = models.ForeignKey(Chapter, 
                                        on_delete= models.SET_NULL,
                                        null = True,
                                        verbose_name ='المحور'
                                        )
    video       = models.URLField(verbose_name = 'رابط فيديو', blank = True)
    links       = models.TextField(blank = True,
                                    verbose_name='روابط مفيدة')
    order       = models.PositiveIntegerField(default = 1, 
                                              verbose_name ='ترتيب الدرس في المحور')
    @property
    def get_links(self):
        ls = self.links.replace(' ','').split('\n')
        while ls.count(''):
            ls.remove('')
        return ls
    #def _get_content_html(self):
        # convert the content into html
    def __str__(self):
        return self.title

    class Meta:
        verbose_name        = 'درس'
        verbose_name_plural = 'دروس'

EX_TYPES = [
    ('one','إختيار إجابة واحدة'),
    ('multiple', 'إختيار إجابات'),
    ('result', 'الإجابة بعدد')
]
EX_POINTS = [
    (3,'3'),
    (6,'6'),
    (9,'9'),
    (12,'12'),
]
class Exercice(models.Model):
    content     = models.TextField(verbose_name ='نص التمرين')
    choices     = models.TextField(verbose_name = 'الاقتراحات', blank = True)
    chapter     = models.ForeignKey(Chapter,verbose_name ='المحور', 
                                on_delete = models.SET_NULL, null = True,)     
    category    = models.CharField( max_length =30,
                                choices = EX_TYPES, 
                                verbose_name ='نوع التمرين')
    solution    = models.CharField( max_length = 20,
                                verbose_name = 'الإجابة')
    explanation = models.TextField(verbose_name = 'شرح الحل', blank = True)
    image       = models.ImageField(blank = True, upload_to = 'exercices_images')
    points      = models.IntegerField(choices = EX_POINTS, default = 3)
    
    def get_choices(self):
        #? result
        return self.choices.strip().split('\n')
    
    #returs the the result as a set of chars
    def get_solution(self):
        return set(self.solution.replace(' ','').split(','))

    def __str__(self):
        return f'تمرين {self.id}: {self.chapter.name}'

    class Meta:
        verbose_name        = 'تمرين'
        verbose_name_plural = 'تمارين'

class ExerciceSolution(models.Model):
    exercice    = models.ForeignKey(Exercice, on_delete = models.CASCADE)
    student     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    correct     = models.BooleanField(default = False)
    answer      = models.CharField(max_length = 30)
    num_of_tries= models.IntegerField(default = 0)

    # def get_answer(self):
    #     return set(self.answer.replace(' ','').split(','))
    
    def add_try(self):
        self.num_of_tries += 1
        self.save()
    class Meta:
        verbose_name        = 'إجابة التمرين'
        verbose_name_plural = 'إجابات التمارين'