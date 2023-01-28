from control.models import Submissions
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordChangeView,
)

from .models import User
from .decorators import cant_use_when_logged

from django.views.generic import (
    DetailView,
    UpdateView,
    ListView,
)
from verify_email.email_handler import send_verification_email

from .forms import SignUpForm


@cant_use_when_logged
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)
            return redirect("/")
    else:
        form = SignUpForm()

    template = "accounts/signup.html"
    return render(request, template, {"form": form})


class LoginView(LoginView):
    template_name = "accounts/login.html"
    extra_context = {"title": "الدخول إلى الموقع", "btn": "تسجيل الدخول"}


class PersonalAccount(UpdateView):
    template_name = "accounts/edit-profile.html"
    model = User
    fields = (
        "first_name",
        "last_name",
        "username_abrv",
        "email",
        "date_of_birth",
        "grade",
        "wilaya",
    )

    success_url = reverse_lazy("accounts:account")
    extra_context = {"btn": "تحديث المعلومات", "profile": True}

    def get_object(self, **kwargs):
        return get_object_or_404(User, pk=self.request.user.id)


@method_decorator(login_required, name="dispatch")
class Profile(DetailView):
    template_name = "accounts/profile.html"
    context_object_name = "progress"

    def get_object(self):
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        return user.progress


class PasswordChangeView(PasswordChangeView):
    template_name = "accounts/edit-profile.html"
    extra_context = {"btn": "تغير كلمة المرور"}
    success_url = reverse_lazy("accounts:account")


@method_decorator(cant_use_when_logged, name="dispatch")
class ResetPW(PasswordResetView):
    template_name = "accounts/login.html"
    email_template_name = "accounts/pw_reset_email.html"
    extra_context = {"title": "إعادة تعيين كلمة السر", "btn": "إرسال"}

    def get_success_url(self):
        return reverse_lazy("accounts:pw_reset_done")


@method_decorator(cant_use_when_logged, name="dispatch")
class ResetPWConfirm(PasswordResetConfirmView):
    template_name = "accounts/login.html"
    extra_context = {"title": "تعيين كلمة المرور الجديدة", "btn": "تعيين كلمة السر"}
    success_url = reverse_lazy("accounts:login")


@method_decorator(cant_use_when_logged, name="dispatch")
class ResetDone(PasswordResetDoneView):
    template_name = "accounts/pw_reset_done.html"


@method_decorator(login_required, name="dispatch")
class StudentsRanking(ListView):
    template_name = "accounts/students-ranking.html"
    model = User
    context_object_name = "students_list"

    def get(self, request, *args, **kwargs):
        Submissions.update_last_correct()
        return super().get(request, *args, **kwargs)
