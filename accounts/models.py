from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings

from lessons.models import Chapter, Exercice
from problems.models import Problem, ProblemSubmission


class UserManager(BaseUserManager):
    def create_user(self, email, password = None, is_active = True, is_staff = False, is_admin = False):
        if not email:
            raise ValueError('لا بد لكل مستخدم من بريد إلكتروني')
        if not password:
            raise ValueError('لا بد لكل مستخدم من كلمة سر')
        user_obj = self.model(
                email = self.normalize_email(email)
        )
        user_obj.set_password(password)
        user_obj.is_active = is_active
        user_obj.is_staff = is_staff
        user_obj.is_admin = is_admin

        user_obj.save(using = self._db)
        return user_obj

    def create_staffuser(self, email, password = None):
        user = self.create_user(
            email,
            password,
            is_staff = True
        )
        return user
    
    def create_superuser(self, email, password = None):
        user = self.create_user(
            email,
            password,
            is_staff = True,
            is_admin = True
        )
        return user

WILAYAS = [(a,a) for a in range(1,49)]
GRADES  = [ (-3, 'السنة 1 متوسط'), 
            (-2, 'السنة 2 متوسط'), 
            (-1, 'السنة 3 متوسط'), 
            (0, 'السنة 4 متوسط'),
            (1, 'السنة 1 ثانوي'), 
            (2, 'السنة 2 ثانوي'), 
            (3, 'السنة 3 ثانوي'),
            (4, 'غير ذلك')
            ]
SEX  = [('m','ذكر'),('f','أنثى'),]
USERNAME_ABRV = [('fl', 'الاسم واللقب'), #first_name+last_name
                ('f', 'الاسم'), #first_name + lastname[0]
                ('l', 'اللقب')
                ]
class User(AbstractBaseUser):
    email           = models.EmailField(max_length = 60, unique = True, verbose_name = 'البريد الإلكتروني')
    first_name      = models.CharField(max_length = 25, verbose_name = 'الاسم')
    last_name       = models.CharField(max_length = 25, verbose_name = 'اللقب')
    date_of_birth   = models.DateField(blank = True, null = True, verbose_name = 'تاريخ الميلاد')
    grade           = models.IntegerField(choices = GRADES, null=True, verbose_name = 'العام الدراسي')
    sex             = models.CharField(choices = SEX, max_length = 2, verbose_name='الجنس')
    wilaya          = models.IntegerField(choices = WILAYAS,null = True, verbose_name = 'ولاية الإقامة')
    join_date       = models.DateField(auto_now_add = True, verbose_name='تاريخ الانضمام')
    username_abrv   = models.CharField(choices = USERNAME_ABRV,verbose_name='طريقة عرض الاسم', default='fl', max_length = 2)
    is_active       = models.BooleanField(default = True) #acitve = can login
    is_staff        = models.BooleanField(default = False)
    is_admin        = models.BooleanField(default = False)
    #is_corrector    = models.BooleanField(default = False)

    
    USERNAME_FIELD = 'email'
    #USERNAME and password are required by default
    REQUIRED_FIELDS = []         #['first_name', 'last_name']

    objects = UserManager()
    def __str__(self):
        return self.email
    def get_full_name(self):
        if first_name or last_name:
            return first_name + ' ' + last_name
        return self.email
    def get_short_name(self):
        if self.username_abrv == 'f':
            return self.first_name + ' ' + self.last_name[0]
        elif self.username_abrv == 'l':
            return self.last_name + ' ' + self.first_name[0]
        return self.first_name + ' ' + self.last_name
    def has_perm(self, perm, obj = None):
        return True
    def has_module_perms(self, app_label):
        return True
    @property
    def username(self):
        if self.username_abrv == 'f':
            return self.first_name + ' ' + self.last_name[0]
        elif self.username_abrv == 'l':
            return self.last_name + ' ' + self.first_name[0]
        return self.first_name + ' ' + self.last_name

class StudentProgress(models.Model):
    student             = models.OneToOneField(settings.AUTH_USER_MODEL,
                                               related_name = 'progress',
                                               on_delete = models.CASCADE
                                               ) #it may be changed
    completed_chapters  = models.ManyToManyField(Chapter, blank = True)
    solved_problems     = models.ManyToManyField(Problem,blank = True)
    solved_exercices    = models.ManyToManyField(Exercice, blank = True)
    last_submissions    = models.ManyToManyField(ProblemSubmission, blank = True)
    points              = models.IntegerField(default = 0, editable = False)
    
    @property
    def rank(self):
        return StudentProgress.objects.filter(points__gt = self.points).count()+1

    def add_points(self, points):
        self.points += points
        self.save()
    #solved problems: either I make a M2M or a method (exercices also)
    
    def opened_problems(self,topic = None):
        if topic:
            chapters = self.completed_chapters.filter(topic = topic)
            problems= Problem.objects.filter(chapter__in = chapters)
        else:
            problems = Problem.objects.filter(chapter__in = self.completed_chapters.all())
        print(problems)
        return problems
