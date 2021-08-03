from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    ProblemsList,
    problem_sub,
    DeleteDraft,
    LastCorrectedSubs,
    LastSolvedProblems
)

app_name = 'problems'

urlpatterns = [
    #path('',)
    path('last-corrected/', LastCorrectedSubs.as_view(), name='last-corrected'),
    path('last-solved/',LastSolvedProblems.as_view(), name='last-solved'),
    path('<slug:slug>/', login_required(ProblemsList.as_view()), name = 'list'),
    path('<slug:slug>/<int:pk>/',login_required(problem_sub), name = 'submit'),
    path('<slug:slug>/<int:pk>/delete/', DeleteDraft.as_view(), name='delete-sub'),

]