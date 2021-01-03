from django.urls import path, reverse_lazy, include
from django.contrib.auth.views import(
    LoginView, 
    LogoutView,
    PasswordChangeView,

)

from .views import( 
    signup,
    Profile,
    PersonalAccount,
    ResetPW,
    ResetPWConfirm,
    ResetDone,
    StudentsRanking,
)

app_name = 'accounts'
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', LoginView.as_view(template_name='accounts/login.html',
                                    extra_context = {'title':'الدخول إلى الموقع',
                                                    'btn':'تسجيل الدخول'}), name='login'),
    path('logout/', LogoutView.as_view(
                            #success_url = '/'
                                    ), name = 'logout'),
    path('myaccount/', PersonalAccount.as_view(), name='account'),
    path('verification/', include('verify_email.urls')),
    path('myaccount/changepw', PasswordChangeView.as_view(
                            template_name='accounts/edit-profile.html',
                            extra_context ={'btn':'تغير كلمة المرور'},
                            success_url = reverse_lazy('accounts:account')
                                                        ), name = 'password_change'),
    path('<int:pk>/',Profile.as_view() , name = 'profile'),
    path('students-ranking/', StudentsRanking.as_view(), name='ranking'),
    path('reset/', ResetPW.as_view(), name='reset-pw'),
    path('reset/done/', ResetDone.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', ResetPWConfirm.as_view(), name='password_reset_confirm'),
]
