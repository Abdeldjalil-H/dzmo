from django.urls import path

from .views import TestAnswerView
app_name = 'tests'
urlpatterns = [
    path('<int:pk>/', TestAnswerView.as_view(), name = 'test'),
]