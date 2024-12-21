from django.contrib.auth.views import LogoutView
from django.urls import include, path

from .views import (
    LoginView,
    PasswordChangeView,
    PersonalAccount,
    Profile,
    ResetDone,
    ResetPW,
    ResetPWConfirm,
    StudentsRanking,
    signup,
)

app_name = "accounts"

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("myaccount/", PersonalAccount.as_view(), name="account"),
    path("verification/", include("verify_email.urls")),
    path("myaccount/changepw", PasswordChangeView.as_view(), name="password_change"),
    path("<int:pk>/", Profile.as_view(), name="profile"),
    path("students-ranking/", StudentsRanking.as_view(), name="ranking"),
    path("reset/", ResetPW.as_view(), name="reset-pw"),
    path("reset/done/", ResetDone.as_view(), name="pw_reset_done"),
    path(
        "reset/<uidb64>/<token>/",
        ResetPWConfirm.as_view(),
        name="password_reset_confirm",
    ),
]
