from django.contrib import admin

from .models import Test, TestAnswer

admin.site.register(Test)
admin.site.register(TestAnswer)