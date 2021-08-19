from django.contrib import admin

from .models import Test, TestAnswer, TestProblem

class ProblemInline(admin.StackedInline):
    model = TestProblem
    extra = 0

class TestAdmin(admin.ModelAdmin):
    inlines = [ProblemInline]
admin.site.register(Test, TestAdmin)
admin.site.register(TestAnswer)