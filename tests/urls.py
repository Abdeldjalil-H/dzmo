from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import TestAnswerView
app_name = 'tests'
urlpatterns = [
    path('<int:pk>/', login_required(TestAnswerView.as_view()), name = 'test'),
]