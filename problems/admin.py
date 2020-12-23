from django.contrib import admin

# Register your models here.
from .models import(
    Problem,
    ProblemSubmission,
    Comment
)

admin.site.register(Problem)
admin.site.register(ProblemSubmission)
admin.site.register(Comment)
