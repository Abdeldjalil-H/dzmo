from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from lessons.models import Chapter, Exercice
from problems.models import Problem, ProblemSubmission, STATUS
from tasks.models import TaskProblemSubmission
TEAMS_COLORS = [('white','white'),
('green', 'green'), ('red','red'), ('black','black')
]
class Team(models.Model):
    color = models.CharField(max_length=100, choices=TEAMS_COLORS, unique=True)

    def __str__(self):
        return f'{self.color} team'

    def get_tasks(self):
        return self.tasks.all()
    
    def get_name(self):
        return self.__str__()
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

WILAYAS = [(a,a) for a in range(1,59)]
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
    is_corrector    = models.BooleanField(default = False)

    team            = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    USERNAME_FIELD  = 'email'
    #USERNAME and password are required by default
    REQUIRED_FIELDS = []         #['first_name', 'last_name']

    objects = UserManager()
    def __str__(self):
        return self.email
    def get_full_name(self):
        if self.first_name or self.last_name:
            return self.first_name + ' ' + self.last_name
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

    def get_solved_problems_by_topic(self, topic):
        return self.progress.solved_problems.filter(chapter__topic=topic)

    def get_opened_problems_by_topic(self, topic):
        return self.progress.opened_problems(topic = topic)
    
    def get_all_subs_by_problem(self, problem):
        return self.submissions.filter(problem=problem)
    def is_tasks_corrector(self):
        return self.is_staff
    def has_solved(self, problem):
        solved = False
        for sub in self.get_all_subs_by_problem(problem):
            solved |= sub.correct
        return solved
    def has_submit(self, problem):
        return self.submissions.filter(problem=problem).exists()
    def add_solved_problem(self, problem):
        self.progress.solved_problems.add(problem)
        for sub in self.get_all_subs_by_problem(problem):
            sub.set_status('correct')
            sub.save()

    def add_points(self, points):
        self.progress.add_points(points)
    def is_team_member(self):
        return self.team is not None

    @property
    def count_last_points(self, period=7):
        start_day = timezone.now() - timedelta(days=period)
        
        return 15 * sum(self.submissions.filter(submited_on__gte=start_day, correct=True).values_list('problem__level', flat=True))
        
    def get_solved_wrong_pending_indicies(self, topic):
        solved = set(self.progress.solved_problems.filter(chapter__topic=topic).values_list('pk', flat=True))
        wrong = set(
            self.submissions.filter(problem__chapter__topic=topic).filter(correct = False).values_list('problem__pk', flat=True)
        )
        #wrong = wrong.difference(solved)
        pending = set(
            self.submissions.filter(problem__chapter__topic=topic).filter(status='submit').values_list('problem__pk', flat=True)
        )
        #pending = pending.difference(wrong)

        return list(solved), list(wrong), list(pending)
    
    def add_task_correction_notif(self, sub):
        self.progress.last_tasks_subs.add(sub)
    def tasks_subs_notif(self):
        return self.progress.last_tasks_subs.count()
    def get_last_tasks_subs(self):
        return self.progress.last_tasks_subs.all()
    class Meta:
        verbose_name        = 'مستخدم'
        verbose_name_plural = 'المستخدمون'

class StudentProgress(models.Model):
    student             = models.OneToOneField(settings.AUTH_USER_MODEL,
                                               related_name = 'progress',
                                               on_delete = models.CASCADE
                                               ) #it may be changed
    completed_chapters  = models.ManyToManyField(Chapter, 
                                            blank = True,
                                            verbose_name='المحاور المتمة'
                                            )
    solved_problems     = models.ManyToManyField(Problem,
                                                blank = True,
                                                verbose_name= 'المسائل المحلولة',
                                                )
    solved_exercices    = models.ManyToManyField(Exercice,
                                                blank = True,
                                                verbose_name = 'التمارين المحلولة',
                                                )
    last_submissions    = models.ManyToManyField(ProblemSubmission, blank = True,
                                                verbose_name = 'آخر المحاولات المقدمة',)
    last_tasks_subs     = models.ManyToManyField(TaskProblemSubmission, blank=True)                                            
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
        return problems

    def __str__(self):
        return self.student.email

    class Meta:
        verbose_name        = 'تقدم التلميذ'
        verbose_name_plural = 'تقدم التلاميذ'
