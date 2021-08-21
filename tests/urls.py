from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    TestAnswerView,
    TestResult,
    TestsList,
    TestAnswersList,
    TestCorrection,
)
app_name = 'tests'
urlpatterns = [
    path('', TestsList.as_view(), name='tests-list'),
    path('<int:pk>/', login_required(TestAnswerView.as_view()), name = 'test'),
    path('<int:pk>/results/', login_required(TestResult.as_view()), name='test-results'),
    path('correction/test<int:test_pk>/', TestAnswersList.as_view(), name='subs-list'),
    path('correction/test<int:test_pk>/pb<int:pb_num>', TestCorrection.as_view(), name='problem-correction'),
]