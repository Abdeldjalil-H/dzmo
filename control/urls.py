from django.urls import path

from .views import(
    SubsList,
    ProblemCorrection,
    AddProblems,
    SendMail,
    TestAnswersList,
    TestCorrection,
)

app_name = 'control'

urlpatterns = [
    path('correction/', SubsList.as_view(), name='subs-list'),
    path('correction/<int:pk>', ProblemCorrection.as_view(), name ='problem-correction'),
    path('add-problems/', AddProblems.as_view(), name='add-problems'),
    path('send-mails/', SendMail.as_view(), name = 'send-mails'),
    path('tests/', TestAnswersList.as_view(), name='test-ans-list'),
    path('tests/<pk>/', TestCorrection.as_view(), name='test-correction'),
]