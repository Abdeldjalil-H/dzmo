from django.urls import path
from .views import (
    TaskPbView,
    TasksList,
    TaskProblemsList,
    TaskPbSubmit,
    TaskSubsList,
    TaskPbsCorrection,
    DeleteSubmission,
    AddProblems,
    LastCorrectedSubs,
    CorrectSolsByTask,
)

app_name = "tasks"

urlpatterns = [
    path("list/", TasksList.as_view(), name="tasks-list"),
    path("task<int:task_pk>/", TaskProblemsList.as_view(), name="problems-list"),
    path(
        "task<int:task_pk>/<int:pb_pk>/sub=0/", TaskPbSubmit.as_view(), name="pb-submit"
    ),
    path("task<int:task_pk>/<int:pb_pk>/", TaskPbView.as_view(), name="pb-view"),
    path(
        "task<int:task_pk>/<int:pb_pk>/delete/",
        DeleteSubmission.as_view(),
        name="delete",
    ),
    # path('correction/list/',name='correction-tasks-list'),
    path(
        "correction/task<int:task_pk>/", TaskSubsList.as_view(), name="task-subs-list"
    ),
    path("correction/task<int:task_pk>/<int:sub_pk>/", TaskPbsCorrection.as_view()),
    path("last-corrected/", LastCorrectedSubs.as_view(), name="last-corrected"),
    path(
        "correct-task<int:task_pk>/", CorrectSolsByTask.as_view(), name="correct-sols"
    ),
    path("add-pbs/", AddProblems.as_view(), name="add-pbs"),
]
