from django.db import models
from django.db.models import Q, Subquery, Sum
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from lessons.models import Chapter, Exercice, TopicField
from problems.models import Problem, ProblemSubmission
from tasks.models import TaskProblemSubmission

TEAMS_COLORS = (
    ("white", "white"),
    ("green", "green"),
    ("red", "red"),
    ("black", "black"),
)


class Team(models.Model):
    color = models.CharField(max_length=100, choices=TEAMS_COLORS, unique=True)

    tasks: models.QuerySet

    def __str__(self):
        return f"{self.color} team"

    def get_tasks(self):
        return self.tasks.all()

    def get_name(self):
        return self.__str__()


class UserManager(BaseUserManager):
    def create_user(
        self, email, password=None, is_active=True, is_staff=False, is_admin=False
    ):
        if not email:
            raise ValueError("لا بد لكل مستخدم من بريد إلكتروني")
        if not password:
            raise ValueError("لا بد لكل مستخدم من كلمة سر")
        user_obj = self.model(email=self.normalize_email(email))
        user_obj.set_password(password)
        user_obj.is_active = is_active
        user_obj.is_staff = is_staff
        user_obj.is_admin = is_admin

        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(email, password, is_staff=True)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password, is_staff=True, is_admin=True)
        return user


WILAYAS = [(a, a) for a in range(1, 59)]
GRADES = (
    (-3, "السنة 1 متوسط"),
    (-2, "السنة 2 متوسط"),
    (-1, "السنة 3 متوسط"),
    (0, "السنة 4 متوسط"),
    (1, "السنة 1 ثانوي"),
    (2, "السنة 2 ثانوي"),
    (3, "السنة 3 ثانوي"),
    (4, "غير ذلك"),
)
SEX = (("m", "ذكر"), ("f", "أنثى"))

USERNAME_ABRV = (
    ("fl", "الاسم واللقب"),  # first_name+last_name
    ("f", "الاسم"),  # first_name + lastname[0]
    ("l", "اللقب"),
)


class User(AbstractBaseUser):
    email = models.EmailField(
        max_length=60, unique=True, verbose_name="البريد الإلكتروني"
    )
    first_name = models.CharField(max_length=25, verbose_name="الاسم")
    last_name = models.CharField(max_length=25, verbose_name="اللقب")
    date_of_birth = models.DateField(
        blank=True, null=True, verbose_name="تاريخ الميلاد"
    )
    grade = models.IntegerField(choices=GRADES, null=True, verbose_name="العام الدراسي")
    sex = models.CharField(choices=SEX, max_length=2, verbose_name="الجنس")
    wilaya = models.IntegerField(
        choices=WILAYAS, null=True, verbose_name="ولاية الإقامة"
    )
    join_date = models.DateField(auto_now_add=True, verbose_name="تاريخ الانضمام")
    username_abrv = models.CharField(
        choices=USERNAME_ABRV,
        verbose_name="طريقة عرض الاسم",
        default="fl",
        max_length=2,
    )
    is_active = models.BooleanField(default=True)  # acitve = can login
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_corrector = models.BooleanField(default=False)

    points = models.IntegerField(default=0, editable=False, db_index=True)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL)
    USERNAME_FIELD = "email"
    # USERNAME and password are required by default
    REQUIRED_FIELDS = []

    completed_chapters = models.ManyToManyField(
        Chapter, blank=True, verbose_name="المحاور المتمة"
    )
    solved_exercices = models.ManyToManyField(
        Exercice, blank=True, verbose_name="التمارين المحلولة"
    )
    last_submissions = models.ManyToManyField(
        ProblemSubmission,
        blank=True,
        verbose_name="آخر المحاولات المقدمة",
    )
    last_tasks_subs = models.ManyToManyField("tasks.TaskProblemSubmission", blank=True)

    submissions: models.QuerySet["ProblemSubmission"]
    tasks_submissions: models.QuerySet["TaskProblemSubmission"]
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.first_name or self.last_name:
            return self.first_name + " " + self.last_name
        return self.email

    def get_short_name(self):
        if self.username_abrv == "f":
            return self.first_name + " " + self.last_name[0]
        elif self.username_abrv == "l":
            return self.last_name + " " + self.first_name[0]
        return self.first_name + " " + self.last_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def username(self):
        if self.username_abrv == "f":
            return self.first_name + " " + self.last_name[0]
        elif self.username_abrv == "l":
            return self.last_name + " " + self.first_name[0]
        return self.first_name + " " + self.last_name

    def get_opened_problems_by_topic(self, topic=None):
        if topic:
            chapters = self.completed_chapters.filter(topic=topic)
            problems = Problem.objects.filter(chapter__in=chapters)
        else:
            problems = Problem.objects.filter(chapter__in=self.completed_chapters.all())
        return problems

    def get_all_subs_by_problem(self, problem):
        return self.submissions.filter(problem=problem)

    def is_tasks_corrector(self):
        return self.is_staff

    def has_submit(self, problem):
        return self.submissions.filter(problem=problem).exists()

    def add_points(self, points):
        self.points += points
        self.save()

    def is_team_member(self):
        return self.team is not None

    def get_school_grade(self):
        return dict(GRADES)[self.grade] if self.grade < 4 else ""

    @property
    def rank(self):
        return User.objects.filter(points__gt=self.points).count() + 1

    @property
    def count_last_points(self, period=7):
        return 15 * (
            (
                ProblemSubmission.correct.last_week()
                .filter(student=self)
                .aggregate(total_level=Sum("problem__level"))["total_level"]
                or 0
            )
            + (
                TaskProblemSubmission.correct.last_week()
                .filter(student=self)
                .aggregate(total_level=Sum("problem__level"))["total_level"]
                or 0
            )
        )

    def get_correct_pks(self, topic):
        return list(
            ProblemSubmission.correct.filter(
                problem__chapter__topic=topic, student=self
            ).values_list("problem_id", flat=True)
        )

    def get_pending_pks(self, topic):
        return list(
            ProblemSubmission.pending.filter(
                student=self, problem__chapter__topic=topic
            ).values_list("problem_id", flat=True)
        )

    def get_wrong_pks(self, topic):
        return list(
            self.submissions.filter(
                status__in=["wrong", "comment"], problem__chapter__topic=topic
            ).values_list("problem_id", flat=True)
        )

    def add_task_correction_notif(self, sub):
        self.last_tasks_subs.add(sub)

    def tasks_subs_notif(self):
        return self.last_tasks_subs.count()

    def get_last_tasks_subs(self):
        return self.last_tasks_subs.all()

    class Meta:
        verbose_name = "مستخدم"
        verbose_name_plural = "المستخدمون"


def default_topics():
    return ["a", "c", "g", "nt", "b"]


class Corrector(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    problems = models.BooleanField(default=True)
    tasks = models.BooleanField(default=False)
    tests = models.BooleanField(default=False)
    self_correction = models.BooleanField(default=False)
    solved_only = models.BooleanField(default=False)
    topics = ArrayField(TopicField(), default=default_topics, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_filters(self):
        q = Q()
        if len(self.topics) != 5:
            q &= Q(problem__chapter__topic__in=self.topics)
        if not self.self_correction:
            q &= ~Q(student=self.user)
        if self.solved_only:
            # TODO: optimize this
            q &= Q(
                problem_id__in=Subquery(
                    ProblemSubmission.correct.filter(student=self.user_id).values_list(
                        "problem_id", flat=True
                    )
                )
            )
        return q

    def can_correct(self, problem):
        return not self.solved_only or (
            problem.chapter.topic in self.topics and problem.has_solved(self.user)
        )
