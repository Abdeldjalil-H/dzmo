from django.contrib import admin

from .models import Test, TestAnswer, TestProblem

class ProblemInline(admin.StackedInline):
    model = TestProblem
    extra = 0

class TestAdmin(admin.ModelAdmin):
    inlines = [ProblemInline]

    def save_model(self, request, obj, form, change):
        obj.number_of_pbs = int(request.POST.get('problems-TOTAL_FORMS'))
        return super().save_model(request, obj, form, change)
admin.site.register(Test, TestAdmin)
admin.site.register(TestAnswer)