from django.contrib import admin

# Register your models here.
from .models import(
    Chapter,
    Lesson,
    Exercice,
    ExerciceSolution
)

admin.site.register(Chapter)
admin.site.register(Lesson)
admin.site.register(Exercice)
admin.site.register(ExerciceSolution)
