from django.contrib import admin

from .models import (
    Task,
    TaskComment,
    TaskProblem,
    TaskProblemSubmission,
)

admin.site.register(Task)
admin.site.register(TaskProblem)
admin.site.register(TaskProblemSubmission)
admin.site.register(TaskComment)
