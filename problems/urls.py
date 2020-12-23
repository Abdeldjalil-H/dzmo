from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    ProblemsList,
    problem_sub,
    DeleteDraft,
    LastCorrectedSubs,
)

app_name = 'problems'

urlpatterns = [
    #path('',)
    path('last-corrected/', LastCorrectedSubs.as_view(), name='last-corrected'),
    path('<slug:slug>/', login_required(ProblemsList.as_view()), name = 'list'),
    path('<slug:slug>/<int:pk>/',login_required(problem_sub), name = 'submit'),
    path('<slug:slug>/<int:pk>/delete', DeleteDraft.as_view(), name='delete-sub'),

]
#chose the problem with chapter and pk otherwise you will see geo in a/5 (example)