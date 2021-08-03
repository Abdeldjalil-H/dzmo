from django.contrib import admin
from .models import (
    Task, 
    TaskProblem, 
    TaskProblemSubmission,
    TaskComment,
)

admin.site.register(Task)
admin.site.register(TaskProblem)
admin.site.register(TaskProblemSubmission)
admin.site.register(TaskComment)