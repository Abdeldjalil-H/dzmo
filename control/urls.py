from django.urls import path

from .views import(
    SubsList,
    ProblemCorrection,
    verify_mail,
)

app_name = 'control'

urlpatterns = [
    path('correction/', SubsList.as_view(), name='subs-list'),
    path('correction/<int:pk>', ProblemCorrection.as_view(), name ='problem-correction'),
    path('verify/', verify_mail, name='verify-mail')
]