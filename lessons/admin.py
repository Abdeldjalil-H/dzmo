from django.contrib import admin

from .models import Chapter, Lesson, Exercice, ExerciceSolution


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 0


class ExerciceInline(admin.StackedInline):
    model = Exercice
    extra = 0


class ChapterAdmin(admin.ModelAdmin):
    inlines = [
        LessonInline,
        ExerciceInline,
    ]

    list_display = ("name", "topic")
    list_filter = (
        "topic",
        "publish",
    )
    search_fields = ("name",)
    ordering = ("topic",)
    # filter_horizontal = ('',)


class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "chapter")
    list_filter = ("chapter",)
    search_fields = ("title",)


class ExerciceAdmin(admin.ModelAdmin):
    list_filter = ("chapter",)


admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Exercice, ExerciceAdmin)
admin.site.register(ExerciceSolution)
