from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    TestAnswerView,
    TestResult,
    TestsList,
    TestAnswersList,
    TestCorrection,
    TestSolution,
    create_test_answer,
    SolutionUploadView,
)

app_name = "tests"

urlpatterns = [
    path(
        "<int:test_pk>/add-answer/",
        login_required(SolutionUploadView.as_view()),
        name="upload-solution",
    ),
    path("", TestsList.as_view(), name="tests-list"),
    path("<int:pk>/", login_required(TestAnswerView.as_view()), name="test"),
    path(
        "<int:test_pk>/create_ans/",
        login_required(create_test_answer),
        name="create_ans",
    ),
    path(
        "<int:test_pk>/results/",
        login_required(TestResult.as_view()),
        name="test-results",
    ),
    path(
        "solution/test<int:test_pk>/",
        login_required(TestSolution.as_view()),
        name="solution",
    ),
    path(
        "correction/test<int:test_pk>/",
        TestAnswersList.as_view(),
        name="subs-list",
    ),
    path(
        "correction/test<int:test_pk>/pb<int:pb_num>",
        TestCorrection.as_view(),
        name="problem-correction",
    ),
]
