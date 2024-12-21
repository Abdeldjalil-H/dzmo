from django.contrib import admin

from .models import Comment, Problem, ProblemSubmission

admin.site.register(Problem)
admin.site.register(ProblemSubmission)
admin.site.register(Comment)
