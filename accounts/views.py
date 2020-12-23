from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import(
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView
)

from .models import User, StudentProgress
from .decorators import cant_use_when_logged
from django.urls import reverse
from django.views.generic import(
    DetailView,
    UpdateView,
    ListView,
)
from verify_email.email_handler import send_verification_email

from .forms import SignUpForm

@cant_use_when_logged
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)
            # form.save()
            # email       = form.cleaned_data.get('email')
            # password    = form.cleaned_data.get('password1')
            # user        = authenticate(username = email, password = password)
            # #login(request, user)
            return redirect ('/')

    else:
        form = SignUpForm()

    template = 'accounts/signup.html'
    return render(request, template, {'form': form})


class PersonalAccount(UpdateView):
    template_name       = 'accounts/edit-profile.html'
    model               = User
    fields              = [ 'first_name',
                            'last_name',
                            'email',
                            'date_of_birth',
                            'grade',
                            'wilaya',
                            ]
    success_url         = reverse_lazy('accounts:account')
    extra_context = {'btn':'تحديث المعلومات', 'profile': True}
    def get_object(self, **kwargs):
        return get_object_or_404(User, pk = self.request.user.id)
        
@method_decorator(login_required, name='dispatch')
class Profile(DetailView):
    template_name       = 'accounts/profile.html'
    model               = StudentProgress
    context_object_name = 'progress'

@method_decorator(cant_use_when_logged, name='dispatch')
class ResetPW(PasswordResetView):
    template_name = 'accounts/login.html'
    extra_context = {'title':'إعادة تعيين كلمة السر','btn':'إرسال'}
    success_url = reverse_lazy('accounts:password_reset_done')

@method_decorator(cant_use_when_logged, name='dispatch')
class ResetPWConfirm(PasswordResetConfirmView):
    template_name       = 'accounts/login.html'
    extra_context       = {'title':'تعيين كلمة المرور الجديدة',
                            'btn': 'تعيين كلمة السر'}
    success_url         = reverse_lazy('accounts:login')

@method_decorator(cant_use_when_logged, name='dispatch')
class ResetDone(PasswordResetDoneView):
    #set a template_name
    pass

@method_decorator(login_required, name='dispatch')
class StudentsRanking(ListView):
    template_name       = 'accounts/students-ranking.html'
    queryset            = User.objects.exclude(is_staff = True)
    context_object_name = 'students_list'

