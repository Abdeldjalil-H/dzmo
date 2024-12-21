from django.contrib import admin

from .models import Problem, ProblemSubmission, Comment

admin.site.register(Problem)
admin.site.register(ProblemSubmission)
admin.site.register(Comment)
