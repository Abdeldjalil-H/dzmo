from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    DeleteSubmission,
    ProblemSubmit,
    ProblemsList,
    LastCorrectedSubs,
    LastSolvedProblems,
    ProblemView,
)

app_name = 'problems'

urlpatterns = [
    path('last-corrected/', LastCorrectedSubs.as_view(), name='last-corrected'),
    path('last-solved/',LastSolvedProblems.as_view(), name='last-solved'),
    path('<slug:topic>/', login_required(ProblemsList.as_view()), name = 'list'),
    path('<slug:topic>/<int:pb_pk>/', ProblemView.as_view(), name='pb-view'),
    path('<slug:topic>/<int:pb_pk>/sub=0/', ProblemSubmit.as_view(), name='submit'),
    path('<slug:topic>/<int:pb_pk>/delete/', DeleteSubmission.as_view(), name='delete-sub'),
]